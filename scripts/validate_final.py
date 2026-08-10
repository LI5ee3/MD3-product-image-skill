#!/usr/bin/env python3
"""Validate the final image for md3-product-image.

Per SKILL.md ("Validate and deliver"), the final file must be an exact portrait
3:4 canvas and pass an Ozon-like 288x384 thumbnail review at 100% without zoom.

This script performs the deterministic checks only:
- the file exists and decodes as an image
- the canvas is an exact 3:4 portrait (any other ratio is a rejection)
- the 288x384 thumbnail is written (LANCZOS) when --output-thumb is given

Visual checks (hierarchy, exact Logo/text, readability, product fidelity,
zones, backings) remain a model judgment pass per the SKILL validation list.

Usage:
  python scripts/validate_final.py --image final.png \\
      [--output-thumb thumb.png] [--thumb-width 288] [--thumb-height 384]

Exit codes: 0 = ratio exact, 1 = any rejection.
Outputs one JSON document on stdout.
"""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

REJECT_RATIO = "CANVAS_NOT_3_4"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True)
    parser.add_argument("--output-thumb", default=None)
    parser.add_argument("--thumb-width", type=int, default=288)
    parser.add_argument("--thumb-height", type=int, default=384)
    args = parser.parse_args()

    image_path = Path(args.image)
    try:
        img = Image.open(image_path)
        img.load()
    except OSError as exc:
        sys.exit(f"IMAGE_UNREADABLE: {exc}")

    w, h = img.size
    ratio_exact = w * 4 == h * 3

    report = {
        "image": str(image_path),
        "size": {"width": w, "height": h},
        "ratio_exact_3_4": ratio_exact,
        "thumbnail": None,
    }

    if args.output_thumb:
        thumb = img.convert("RGB").resize(
            (args.thumb_width, args.thumb_height), Image.LANCZOS
        )
        thumb.save(args.output_thumb, "PNG")
        report["thumbnail"] = {
            "path": args.output_thumb,
            "size": {"width": args.thumb_width, "height": args.thumb_height},
        }

    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    print()

    if not ratio_exact:
        sys.exit(REJECT_RATIO)


if __name__ == "__main__":
    main()
