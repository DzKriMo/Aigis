from fastapi import FastAPI
from ..app import app

# re-export for uvicorn entrypoint
__all__ = ["app"]
