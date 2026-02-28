from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from ..policies.engine import PolicyEngine
from ..policies.loader import load_policies
from ..detectors.registry import DetectorRegistry
from ..prellm.normalize import normalize_text
from ..prellm.network import evaluate_urls
from ..postllm.approval import approval_hash
from .tool_router import execute_tool

@dataclass
class RuntimeResult:
    output: str
    actions: List[str]
    risk_score: float
    message: Optional[str]
    approval_hash: Optional[str]
    metadata: Dict[str, Any]

class GuardedRuntime:
    def __init__(self, store):
        self.store = store
        self.detectors = DetectorRegistry.default()
        self.policy_engine = PolicyEngine(load_policies())

    def handle_user_message(
        self,
        session_id: str,
        content: str,
        metadata: Dict[str, Any],
        tenant_id: Optional[str] = None,
        role: Optional[str] = None,
        environment: Optional[str] = None,
        labels: Optional[List[str]] = None,
        url_allowlist: Optional[List[str]] = None,
        url_denylist: Optional[List[str]] = None,
        urls: Optional[List[str]] = None,
    ) -> RuntimeResult:
        labels = labels or []
        url_allowlist = url_allowlist or []
        url_denylist = url_denylist or []
        urls = urls or []

        context = {
            "tenant_id": tenant_id,
            "role": role,
            "environment": environment,
            "labels": labels,
            "metadata": metadata,
        }

        # 0) normalize input
        normalized, norm_flags = normalize_text(content)
        if norm_flags:
            self.store.log_event(session_id, {
                "stage": "prellm.normalize",
                "content": content,
                "normalized": normalized,
                "flags": norm_flags,
            })

        # 1) pre-LLM network firewall (if URLs provided)
        if urls:
            net_decision = evaluate_urls(urls, allowlist=url_allowlist, denylist=url_denylist)
            self.store.log_event(session_id, {
                "stage": "prellm.network",
                "urls": urls,
                "decision": net_decision.to_dict(),
            })
            if net_decision.blocked:
                return RuntimeResult(
                    output=net_decision.message or "Blocked",
                    actions=["block"],
                    risk_score=net_decision.risk_score,
                    message=net_decision.message,
                    approval_hash=None,
                    metadata={},
                )

        # 2) policy evaluate input
        decision = self.policy_engine.evaluate(normalized, stage="prellm", detectors=self.detectors, context=context)
        self.store.log_event(session_id, {
            "stage": "prellm",
            "content": normalized,
            "decision": decision.to_dict(),
        })
        if decision.blocked:
            return RuntimeResult(
                output=decision.message or "Blocked",
                actions=["block"],
                risk_score=decision.risk_score,
                message=decision.message,
                approval_hash=None,
                metadata={},
            )
        if decision.require_approval:
            h = approval_hash(stage="prellm", content=normalized, context=context)
            if not self.store.is_approved(session_id, h):
                self.store.add_pending_approval(session_id, h)
                return RuntimeResult(
                    output=decision.message or "Approval required",
                    actions=["require_approval"],
                    risk_score=decision.risk_score,
                    message=decision.message,
                    approval_hash=h,
                    metadata={},
                )

        # 3) placeholder model response
        model_output = f"Echo: {normalized}"

        # 4) post-LLM policy evaluate
        out_decision = self.policy_engine.evaluate(model_output, stage="postllm", detectors=self.detectors, context=context)
        self.store.log_event(session_id, {
            "stage": "postllm",
            "content": model_output,
            "decision": out_decision.to_dict(),
        })

        if out_decision.require_approval:
            h = approval_hash(stage="postllm", content=model_output, context=context)
            if not self.store.is_approved(session_id, h):
                self.store.add_pending_approval(session_id, h)
                return RuntimeResult(
                    output=out_decision.message or "Approval required",
                    actions=["require_approval"],
                    risk_score=out_decision.risk_score,
                    message=out_decision.message,
                    approval_hash=h,
                    metadata={},
                )
        if out_decision.blocked:
            return RuntimeResult(
                output=out_decision.message or "Blocked",
                actions=["block"],
                risk_score=out_decision.risk_score,
                message=out_decision.message,
                approval_hash=None,
                metadata={},
            )

        output = out_decision.apply_redaction(model_output)
        if out_decision.modified_text is not None:
            output = out_decision.modified_text

        actions = out_decision.actions()
        return RuntimeResult(
            output=output,
            actions=actions,
            risk_score=out_decision.risk_score,
            message=out_decision.message,
            approval_hash=None,
            metadata={},
        )

    def handle_tool_call(
        self,
        session_id: str,
        tool_name: str,
        payload: Dict[str, Any],
        environment: Optional[str],
        allowlist: Optional[List[str]],
        denylist: Optional[List[str]],
        filesystem_root: Optional[str],
        tenant_id: Optional[str] = None,
        role: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        labels = labels or []
        context = {
            "tenant_id": tenant_id,
            "role": role,
            "environment": environment,
            "labels": labels,
            "metadata": {},
        }

        pre_decision = self.policy_engine.evaluate(
            text=f"{tool_name}:{payload}",
            stage="tool_pre",
            detectors=self.detectors,
            context=context,
        )
        self.store.log_event(session_id, {
            "stage": "tool_pre",
            "tool": tool_name,
            "payload": payload,
            "decision": pre_decision.to_dict(),
        })
        if pre_decision.blocked:
            return {
                "allowed": False,
                "message": pre_decision.message or "Tool blocked",
                "result": None,
            }
        if pre_decision.require_approval:
            h = approval_hash(stage="tool_pre", content=f"{tool_name}:{payload}", context=context)
            if not self.store.is_approved(session_id, h):
                self.store.add_pending_approval(session_id, h)
                return {
                    "allowed": False,
                    "message": pre_decision.message or "Approval required",
                    "result": None,
                    "approval_hash": h,
                }

        result = execute_tool(
            tool_name=tool_name,
            payload=payload,
            environment=environment,
            allowlist=allowlist,
            denylist=denylist,
            filesystem_root=filesystem_root,
        )
        self.store.log_event(session_id, {
            "stage": "tool_exec",
            "tool": tool_name,
            "payload": payload,
            "allowed": result.allowed,
            "message": result.message,
        })

        post_decision = self.policy_engine.evaluate(
            text=f"{tool_name}:{result.result}",
            stage="tool_post",
            detectors=self.detectors,
            context=context,
        )
        self.store.log_event(session_id, {
            "stage": "tool_post",
            "tool": tool_name,
            "result": result.result,
            "decision": post_decision.to_dict(),
        })
        if post_decision.blocked:
            return {
                "allowed": False,
                "message": post_decision.message or "Tool result blocked",
                "result": None,
            }
        if post_decision.require_approval:
            h = approval_hash(stage="tool_post", content=f"{tool_name}:{result.result}", context=context)
            if not self.store.is_approved(session_id, h):
                self.store.add_pending_approval(session_id, h)
                return {
                    "allowed": False,
                    "message": post_decision.message or "Approval required",
                    "result": None,
                    "approval_hash": h,
                }

        return {
            "allowed": result.allowed,
            "message": result.message,
            "result": result.result,
        }
