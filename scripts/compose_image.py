#!/usr/bin/env python3
"""Apply cached Logo and text assets to a prepared product scene."""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image


TITLE_COLOR = (44, 44, 44)
VERSION_COLOR = (90, 90, 90)
OUTPUT_KINDS = ("CANDIDATE", "SKU_PREVIEW")


def load_image(path: Path, mode: str) -> Image.Image:
    try:
        with Image.open(path) as source:
            image = source.convert(mode)
            image.load()
            return image
    except OSError as exc:
        raise ValueError(f"ASSET_UNREADABLE: {path}: {exc}") from exc


def target_box(rect: dict, width: int, height: int) -> tuple[int, int, int, int]:
    try:
        left = round(float(rect["x"]) * width)
        top = round(float(rect["y"]) * height)
        target_width = max(1, round(float(rect["w"]) * width))
        target_height = max(1, round(float(rect["h"]) * height))
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("LAYOUT_RECT_INVALID") from exc
    if left < 0 or top < 0 or left + target_width > width or top + target_height > height:
        raise ValueError("LAYOUT_RECT_OUTSIDE_CANVAS")
    return left, top, target_width, target_height


def asset_path(reusable_dir: Path, rect: dict) -> Path:
    try:
        path = (reusable_dir / rect["asset"]).resolve()
    except (KeyError, TypeError) as exc:
        raise ValueError("LAYOUT_ASSET_INVALID") from exc
    if path.parent != reusable_dir:
        raise ValueError("LAYOUT_ASSET_OUTSIDE_REUSABLE")
    return path


def paste_layer(
    scene: Image.Image,
    reusable_dir: Path,
    rect: dict,
    color: tuple[int, int, int] | None,
    width: int,
    height: int,
) -> None:
    left, top, target_width, target_height = target_box(rect, width, height)
    layer = load_image(asset_path(reusable_dir, rect), "L" if color else "RGBA").resize(
        (target_width, target_height), Image.Resampling.LANCZOS
    )
    if color:
        mask = layer
        layer = Image.new("RGBA", mask.size, color + (255,))
        layer.putalpha(mask)
    scene.alpha_composite(layer, (left, top))


def validate_output(kind: str, output: Path, product_dir: Path) -> None:
    if output.parent != product_dir or output.suffix.lower() != ".png":
        raise ValueError("OUTPUT_PATH_INVALID")
    if kind == "CANDIDATE":
        valid = output.name.startswith("master-candidate-") and not output.name.endswith("-scene.png")
    else:
        valid = output.name.startswith("SKU_VARIANT-") and output.name.endswith("-preview.png")
    if not valid:
        raise ValueError(f"{kind}_PATH_INVALID")
    if output.exists():
        raise ValueError(f"REFUSE_OVERWRITE: {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene", required=True)
    parser.add_argument("--layout", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--output-kind", required=True, choices=OUTPUT_KINDS)
    args = parser.parse_args()

    scene_path = Path(args.scene).expanduser().resolve()
    layout_path = Path(args.layout).expanduser().resolve()
    reusable_dir = layout_path.parent
    product_dir = reusable_dir.parent
    output = Path(args.output).expanduser().resolve()

    try:
        if layout_path != product_dir / "reusable" / "layout.json":
            raise ValueError("LAYOUT_PATH_INVALID")
        if scene_path.parent != product_dir:
            raise ValueError("SCENE_OUTSIDE_PRODUCT_DIRECTORY")
        validate_output(args.output_kind, output, product_dir)
        with layout_path.open(encoding="utf-8") as handle:
            layout = json.load(handle)
        if layout.get("product_directory") != str(product_dir):
            raise ValueError("PRODUCT_DIRECTORY_MISMATCH")
        scene = load_image(scene_path, "RGBA")
        width, height = scene.size
        if width * 4 != height * 3 or layout.get("canvas", {}).get("ratio") != "3:4":
            raise ValueError("SCENE_NOT_3_4")
        elements = layout["elements"]
        logo_rect = elements["LOGO_RECT"]
        title_rects = elements["TITLE_LINE_RECT"]
        version_rect = elements.get("VERSION_TEXT_RECT")
        paste_layer(scene, reusable_dir, logo_rect, None, width, height)
        for rect in title_rects:
            paste_layer(scene, reusable_dir, rect, TITLE_COLOR, width, height)
        if version_rect:
            paste_layer(scene, reusable_dir, version_rect, VERSION_COLOR, width, height)
        scene.convert("RGB").save(output, "PNG")
    except (KeyError, TypeError, OSError, json.JSONDecodeError, ValueError) as exc:
        sys.exit(str(exc))

    json.dump(
        {
            "output": str(output),
            "output_kind": args.output_kind,
            "title_color": "2C2C2C",
            "version_color": "5A5A5A" if version_rect else None,
        },
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )
    print()


if __name__ == "__main__":
    main()
