#!/usr/bin/env python3
"""Validate an MD3 candidate, SKU preview, or final image."""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--image-kind", required=True, choices=("CANDIDATE", "SKU_PREVIEW", "FINAL")
    )
    parser.add_argument("--image", required=True)
    args = parser.parse_args()
    path = Path(args.image).expanduser().resolve()

    valid_name = {
        "CANDIDATE": path.name.startswith("master-candidate-")
        and not path.name.endswith("-scene.png"),
        "SKU_PREVIEW": path.name.startswith("SKU_VARIANT-")
        and path.name.endswith("-preview.png"),
        "FINAL": path.name == "ORIGINAL_MASTER_FINAL.png"
        or path.name.startswith("SKU_VARIANT-") and path.suffix.lower() == ".png",
    }[args.image_kind]
    if path.suffix.lower() != ".png" or not valid_name:
        sys.exit(f"{args.image_kind}_FILENAME_INVALID")
    if args.image_kind == "FINAL" and path.parent.name != "output":
        sys.exit("FINAL_OUTSIDE_PRODUCT_OUTPUT_DIRECTORY")

    try:
        with Image.open(path) as image:
            image.load()
            width, height = image.size
    except OSError as exc:
        sys.exit(f"IMAGE_UNREADABLE: {exc}")
    if width * 4 != height * 3:
        sys.exit("CANVAS_NOT_3_4")

    json.dump(
        {
            "image": str(path),
            "image_kind": args.image_kind,
            "size": {"width": width, "height": height},
            "ratio_exact_3_4": True,
        },
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )
    print()


if __name__ == "__main__":
    main()
