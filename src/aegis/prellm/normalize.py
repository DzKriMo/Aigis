import unicodedata

# Format and control characters are commonly used for prompt obfuscation.
INVISIBLE_CATEGORIES = {"Cf"}

# Keep common whitespace control chars; strip other control chars.
ALLOWED_CONTROL_CHARS = {"\n", "\r", "\t"}

# Common Cyrillic/Greek confusables used in prompt obfuscation.
CONFUSABLES_MAP = {
    # Greek
    "Α": "A", "Β": "B", "Ε": "E", "Ζ": "Z", "Η": "H", "Ι": "I", "Κ": "K", "Μ": "M", "Ν": "N", "Ο": "O", "Ρ": "P", "Τ": "T", "Υ": "Y", "Χ": "X",
    "α": "a", "β": "b", "γ": "y", "δ": "d", "ε": "e", "ι": "i", "κ": "k", "ν": "v", "ο": "o", "ρ": "p", "τ": "t", "υ": "u", "χ": "x",
    # Cyrillic
    "А": "A", "В": "B", "Е": "E", "К": "K", "М": "M", "Н": "H", "О": "O", "Р": "P", "С": "C", "Т": "T", "Х": "X", "У": "Y",
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y", "х": "x", "к": "k", "м": "m", "н": "h", "т": "t", "в": "b",
}


def _strip_invisible_and_controls(text: str) -> str:
    out = []
    for ch in text:
        cat = unicodedata.category(ch)
        if cat in INVISIBLE_CATEGORIES:
            continue
        if cat == "Cc" and ch not in ALLOWED_CONTROL_CHARS:
            continue
        out.append(ch)
    return "".join(out)


def _deobfuscate_homoglyphs(text: str) -> str:
    return "".join(CONFUSABLES_MAP.get(ch, ch) for ch in text)


def normalize_text(text: str):
    normalized = unicodedata.normalize("NFKC", text)
    stripped = _strip_invisible_and_controls(normalized)
    deobfuscated = _deobfuscate_homoglyphs(stripped)

    flags = []
    if normalized != text:
        flags.append("normalized_nfkc")
    if stripped != normalized:
        flags.append("removed_invisible_or_control")
    if deobfuscated != stripped:
        flags.append("mapped_confusables")

    return deobfuscated, flags
