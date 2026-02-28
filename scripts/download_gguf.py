# Download a GGUF model from Hugging Face for llama.cpp
# Usage: python scripts/download_gguf.py <repo> <filename> [dest_dir]

import os
import sys
from huggingface_hub import hf_hub_download


def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/download_gguf.py <repo> <filename> [dest_dir]")
        return 1
    repo = sys.argv[1]
    filename = sys.argv[2]
    dest_dir = sys.argv[3] if len(sys.argv) > 3 else "models"

    os.makedirs(dest_dir, exist_ok=True)
    path = hf_hub_download(repo_id=repo, filename=filename, local_dir=dest_dir, local_dir_use_symlinks=False)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
