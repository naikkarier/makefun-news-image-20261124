"""Copy the 24 November 2026 front page into the output directory.

The repository holds the finished image as entry.png. This program
checks the image (PNG, 1024 by 1024, at most 1 MiB, not empty) and
copies it to the directory the harness reads. It touches no network
and uses no randomness, so repeated runs produce identical output.
The destination defaults to /output and can be overridden with the
MAKEFUN_OUTPUT_DIR environment variable.
"""
import os
import shutil
import struct
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
DEST_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024
EXPECTED_SIZE = (1024, 1024)


def read_dimensions(path: Path) -> tuple:
    """Return (width, height) of a PNG, rejecting anything else."""
    with path.open("rb") as handle:
        head = handle.read(33)
    if head[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG file")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit("entry.png is missing from the repository")
    byte_count = SOURCE.stat().st_size
    if byte_count == 0:
        raise SystemExit("entry.png is empty")
    if byte_count > MAX_BYTES:
        raise SystemExit("entry.png must be at most 1 MiB")
    size = read_dimensions(SOURCE)
    if size != EXPECTED_SIZE:
        raise SystemExit(
            "entry.png must be 1024x1024, got %dx%d" % (size[0], size[1])
        )
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    target = DEST_DIR / "entry.png"
    shutil.copyfile(SOURCE, target)
    if target.stat().st_size != byte_count:
        raise SystemExit("copy of entry.png came out the wrong size")
    if read_dimensions(target) != EXPECTED_SIZE:
        raise SystemExit("copy of entry.png has the wrong dimensions")


if __name__ == "__main__":
    main()
