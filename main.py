"""Sum up 24 November's world news in one image.

The program copies the front-page image held in this repository to
the output directory. No network, no randomness, no input: two runs
write the same bytes. The output directory is /output unless the
MAKEFUN_OUTPUT_DIR environment variable names another one.
"""
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def _png_size(path: str) -> tuple:
    with open(path, "rb") as fh:
        header = fh.read(33)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main() -> None:
    if not os.path.isfile(SOURCE):
        raise SystemExit("entry.png is missing from the repository")
    size = os.path.getsize(SOURCE)
    if size == 0 or size > 1024 * 1024:
        raise SystemExit("entry.png must be non-empty and at most 1 MiB")
    width, height = _png_size(SOURCE)
    if (width, height) != (1024, 1024):
        raise SystemExit("entry.png must be 1024x1024, got %dx%d" % (width, height))
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    dest = os.path.join(OUTPUT_DIR, "entry.png")
    shutil.copyfile(SOURCE, dest)
    if os.path.getsize(dest) != size:
        raise SystemExit("copy of entry.png came out the wrong size")


if __name__ == "__main__":
    main()
