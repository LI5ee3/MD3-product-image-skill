#!/usr/bin/env python3
"""Validate a candidate or final image for md3-product-image.

The file must be an exact portrait 3:4 canvas and pass a 288x384 thumbnail
review at 100% without zoom.

This script performs the deterministic checks only:
- the file exists and decodes as an image
- the canvas is an exact 3:4 portrait (any other ratio is a rejection)
- the 288x384 thumbnail is written directly in the product directory when
  --output-thumb is given; the output folder is forbidden

Visual checks (hierarchy, exact Logo/text, readability, product fidelity,
zones, backings) remain a model judgment pass per the SKILL validation list.

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

    if (
        not image_path.name.startswith("master-candidate-")
        or image_path.name == "master-candidate-.png"
        or image_path.suffix.lower() != ".png"
        or image_path.name.endswith(("-scene.png", "-thumb.png"))
    ):
        raise ValueError("CANDIDATE_FILENAME_INVALID")
    return image_path.parent


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image-kind", required=True, choices=("CANDIDATE", "FINAL"))
    parser.add_argument("--image", required=True)
    parser.add_argument("--output-thumb", default=None)
    parser.add_argument("--thumb-width", type=int, default=288)
    parser.add_argument("--thumb-height", type=int, default=384)
    args = parser.parse_args()

    image_path = Path(args.image).expanduser().resolve()
    try:
        product_dir = resolve_product_dir(image_path, args.image_kind)
    except ValueError as exc:
        sys.exit(str(exc))
    if (
        args.thumb_width <= 0
        or args.thumb_height <= 0
        or args.thumb_width * 4 != args.thumb_height * 3
    ):
        sys.exit("THUMBNAIL_NOT_3_4")
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
        "thumbnail": None,
    }

    if args.output_thumb:
        thumb_path = Path(args.output_thumb).expanduser().resolve()
        if thumb_path.parent != product_dir:
            sys.exit("THUMBNAIL_MUST_BE_IN_PRODUCT_DIRECTORY")
        expected_thumb = product_dir / f"{image_path.stem}-thumb.png"
        if thumb_path != expected_thumb:
            sys.exit(f"THUMBNAIL_FILENAME_INVALID: expected {expected_thumb.name}")
        if thumb_path.exists():
            sys.exit(f"REFUSE_OVERWRITE: {thumb_path}")
        thumb = img.convert("RGB").resize(
            (args.thumb_width, args.thumb_height), Image.LANCZOS
        )
        thumb.save(thumb_path, "PNG")
        report["thumbnail"] = {
            "path": str(thumb_path),
            "size": {"width": args.thumb_width, "height": args.thumb_height},
        }

    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    print()

    if not ratio_exact:
        sys.exit(REJECT_RATIO)


if __name__ == "__main__":
    main()
