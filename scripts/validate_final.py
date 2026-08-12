#!/usr/bin/env python3
"""Validate a candidate, SKU preview, or final image for md3-product-image.

This script performs the deterministic checks only:
- the file exists and decodes as an image
- the canvas is an exact 3:4 portrait (any other ratio is a rejection)
Visual checks remain the user's decision after the full-size composite is shown.

Usage:
  python scripts/validate_final.py --image-kind FINAL --image PRODUCT/output/final.png

Exit codes: 0 = ratio exact, 1 = any rejection.
Outputs one JSON document on stdout.
"""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

REJECT_RATIO = "CANVAS_NOT_3_4"


def resolve_product_dir(image_path: Path, image_kind: str) -> Path:
    if image_kind == "FINAL":
        if image_path.parent.name != "output":
            raise ValueError("FINAL_OUTSIDE_PRODUCT_OUTPUT_DIRECTORY")
        allowed = image_path.name == "ORIGINAL_MASTER_FINAL.png" or (
            image_path.name.startswith("SKU_VARIANT-")
            and image_path.name != "SKU_VARIANT-.png"
            and image_path.suffix.lower() == ".png"
        )
        if not allowed:
            raise ValueError("FINAL_FILENAME_INVALID")
        return image_path.parent.parent

    if image_kind == "SKU_PREVIEW":
        if (
            not image_path.name.startswith("SKU_VARIANT-")
            or not image_path.name.endswith("-preview.png")
        ):
            raise ValueError("SKU_PREVIEW_FILENAME_INVALID")
        return image_path.parent

    if (
        not image_path.name.startswith("master-candidate-")
        or image_path.name == "master-candidate-.png"
        or image_path.suffix.lower() != ".png"
        or image_path.name.endswith("-scene.png")
    ):
        raise ValueError("CANDIDATE_FILENAME_INVALID")
    return image_path.parent


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--image-kind", required=True, choices=("CANDIDATE", "SKU_PREVIEW", "FINAL")
    )
    parser.add_argument("--image", required=True)
    args = parser.parse_args()

    image_path = Path(args.image).expanduser().resolve()
    try:
        product_dir = resolve_product_dir(image_path, args.image_kind)
    except ValueError as exc:
        sys.exit(str(exc))
    try:
        img = Image.open(image_path)
        img.load()
    except OSError as exc:
        sys.exit(f"IMAGE_UNREADABLE: {exc}")

    w, h = img.size
    ratio_exact = w * 4 == h * 3

    report = {
        "image": str(image_path),
        "image_kind": args.image_kind,
        "size": {"width": w, "height": h},
        "ratio_exact_3_4": ratio_exact,
    }

    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    print()

    if not ratio_exact:
        sys.exit(REJECT_RATIO)


if __name__ == "__main__":
    main()
