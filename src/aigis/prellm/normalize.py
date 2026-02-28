import unicodedata

INVISIBLE_CATEGORIES = {"Cf"}


def normalize_text(text: str):
    normalized = unicodedata.normalize("NFKC", text)
    stripped = "".join(ch for ch in normalized if unicodedata.category(ch) not in INVISIBLE_CATEGORIES)
    flags = []
    if normalized != text:
        flags.append("normalized_nfkc")
    if stripped != normalized:
        flags.append("removed_invisible")
    return stripped, flags
