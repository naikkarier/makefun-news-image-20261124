"""Sum up 24 November's world news in one image.

The program copies the front-page image held in this repository to
/output/entry.png. No network, no randomness, no input: two runs write
the same bytes.
"""
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


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
    if os.path.getsize(SOURCE) > 1024 * 1024:
        raise SystemExit("entry.png must be at most 1 MiB")
    width, height = _png_size(SOURCE)
    if (width, height) != (1024, 1024):
        raise SystemExit("entry.png must be 1024x1024, got %dx%d" % (width, height))
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SOURCE, "/output/entry.png")


if __name__ == "__main__":
    main()
