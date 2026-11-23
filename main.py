"""
main.py – make.fun entry runner (standard library only)
Copies the pre-generated entry.png to MAKEFUN_OUTPUT_DIR.
Idempotent: identical output on every run.
"""
import os
import shutil
import sys


def main():
    here    = os.path.dirname(os.path.abspath(__file__))
    src     = os.path.join(here, "entry.png")

    if not os.path.isfile(src):
        print(
            f"ERROR: {src} not found. "
            "Run  python make_image.py  first to generate entry.png.",
            file=sys.stderr,
        )
        sys.exit(1)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    os.makedirs(out_dir, exist_ok=True)

    dst = os.path.join(out_dir, "entry.png")
    shutil.copy2(src, dst)
    print(f"OK  entry.png  ->  {dst}")


if __name__ == "__main__":
    main()
