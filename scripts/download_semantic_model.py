import os
import sys


def main():
    try:
        from sentence_transformers import SentenceTransformer  # type: ignore
    except Exception:
        print("sentence-transformers not installed. Run: pip install -r requirements-ml.txt")
        return 1

    model_id = os.getenv("AIGIS_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    print(f"Downloading model: {model_id}")
    SentenceTransformer(model_id)
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
