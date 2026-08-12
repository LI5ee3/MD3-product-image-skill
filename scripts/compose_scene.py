#!/usr/bin/env python3
"""Composite a transparent product and one deterministic 2D shadow onto a background."""

import argparse
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter


ANGLE_DEGREES = 50
PRODUCT_HEIGHT_FRAC = 0.54
PRODUCT_MAX_WIDTH_FRAC = 0.52
WIDE_PRODUCT_ASPECT = 1.35
WIDE_PRODUCT_MAX_WIDTH_FRAC = 0.68
TALL_PRODUCT_ASPECT = 0.90
PRODUCT_RIGHT_MARGIN_FRAC = 0.12
PRODUCT_BOTTOM_MARGIN_FRAC = 0.18
TALL_PRODUCT_BOTTOM_MARGIN_FRAC = 0.12
SHADOW_DISTANCE_FRAC = 0.16
SHADOW_BLUR_FRAC = 0.007
SHADOW_OPACITY = 0.28
PRODUCT_ALPHA_CORE = 224


def load(path: Path, mode: str) -> Image.Image:
    try:
        with Image.open(path) as source:
            image = source.convert(mode)
            image.load()
            return image
    except OSError as exc:
        raise ValueError(f"IMAGE_UNREADABLE: {path}: {exc}") from exc


def new_output(path: Path) -> None:
    if path.exists():
        raise ValueError(f"REFUSE_OVERWRITE: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)


def clean_product(product: Image.Image) -> Image.Image:
    alpha = product.getchannel("A")
    if alpha.getextrema() == (255, 255):
        raise ValueError("PRODUCT_TRANSPARENCY_REQUIRED")
    core = alpha.point(lambda value: 255 if value >= PRODUCT_ALPHA_CORE else 0)
    bbox = core.getbbox()
    if bbox is None:
        raise ValueError("PRODUCT_ALPHA_EMPTY")
    expansion = max(3, round(min(product.size) * 0.004))
    if expansion % 2 == 0:
        expansion += 1
    keep = core.filter(ImageFilter.MaxFilter(expansion))
    cleaned = product.copy()
    cleaned.putalpha(ImageChops.multiply(alpha, keep))
    bbox = cleaned.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("PRODUCT_ALPHA_EMPTY")
    return cleaned.crop(bbox)


def placement_profile(aspect: float) -> tuple[str, float, float]:
    if aspect >= WIDE_PRODUCT_ASPECT:
        return "WIDE", WIDE_PRODUCT_MAX_WIDTH_FRAC, PRODUCT_BOTTOM_MARGIN_FRAC
    if aspect < TALL_PRODUCT_ASPECT:
        return "TALL", PRODUCT_MAX_WIDTH_FRAC, TALL_PRODUCT_BOTTOM_MARGIN_FRAC
    return "STANDARD", PRODUCT_MAX_WIDTH_FRAC, PRODUCT_BOTTOM_MARGIN_FRAC


def fit_product(
    product: Image.Image, width: int, height: int, max_width_frac: float
) -> Image.Image:
    scale = min(
        height * PRODUCT_HEIGHT_FRAC / product.height,
        width * max_width_frac / product.width,
    )
    size = (max(1, round(product.width * scale)), max(1, round(product.height * scale)))
    return product.resize(size, Image.Resampling.LANCZOS)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--background", required=True)
    parser.add_argument("--product", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--product-layer", required=True)
    parser.add_argument("--shadow-mask", required=True)
    parser.add_argument("--reuse-layers", action="store_true")
    args = parser.parse_args()

    background_path = Path(args.background).expanduser().resolve()
    product_path = Path(args.product).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    product_layer_path = Path(args.product_layer).expanduser().resolve()
    shadow_mask_path = Path(args.shadow_mask).expanduser().resolve()

    try:
        background = load(background_path, "RGBA")
        width, height = background.size
        if width * 4 != height * 3:
            raise ValueError(f"BACKGROUND_NOT_3_4: got {width}x{height}")
        if args.reuse_layers:
            product_layer = load(product_layer_path, "RGBA")
            shadow = load(shadow_mask_path, "L")
            if product_layer.size != background.size or shadow.size != background.size:
                raise ValueError("CACHED_LAYER_SIZE_MISMATCH")
            bbox = product_layer.getchannel("A").getbbox()
            if bbox is None:
                raise ValueError("CACHED_PRODUCT_LAYER_EMPTY")
            left, top, right, bottom = bbox
            source_aspect = (right - left) / (bottom - top)
            profile, max_width_frac, bottom_margin_frac = placement_profile(source_aspect)
            distance = (bottom - top) * SHADOW_DISTANCE_FRAC
            radians = math.radians(ANGLE_DEGREES)
            offset_x = round(distance * math.cos(radians))
            offset_y = round(distance * math.sin(radians))
            blur = max(1, round(height * SHADOW_BLUR_FRAC))
        else:
            product = clean_product(load(product_path, "RGBA"))
            source_aspect = product.width / product.height
            profile, max_width_frac, bottom_margin_frac = placement_profile(source_aspect)
            product = fit_product(product, *background.size, max_width_frac)
            right = width - round(width * PRODUCT_RIGHT_MARGIN_FRAC)
            bottom = height - round(height * bottom_margin_frac)
            left = right - product.width
            top = bottom - product.height
            if left < 0 or top < 0:
                raise ValueError("PRODUCT_PLACEMENT_OUTSIDE_CANVAS")
            product_layer = Image.new("RGBA", background.size, (0, 0, 0, 0))
            product_layer.alpha_composite(product, (left, top))
            product_mask = product_layer.getchannel("A")
            distance = product.height * SHADOW_DISTANCE_FRAC
            radians = math.radians(ANGLE_DEGREES)
            offset_x = round(distance * math.cos(radians))
            offset_y = round(distance * math.sin(radians))
            shadow = Image.new("L", background.size, 0)
            shadow.paste(product_mask, (offset_x, offset_y))
            blur = max(1, round(height * SHADOW_BLUR_FRAC))
            shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
            shadow = shadow.point(lambda value: round(value * SHADOW_OPACITY))

        shadow_layer = Image.new("RGBA", background.size, (0, 0, 0, 0))
        shadow_layer.putalpha(shadow)
        scene = Image.alpha_composite(background, shadow_layer)
        scene = Image.alpha_composite(scene, product_layer).convert("RGB")

        new_output(output_path)
        scene.save(output_path, "PNG")
        if not args.reuse_layers:
            for path in (product_layer_path, shadow_mask_path):
                new_output(path)
            product_layer.save(product_layer_path, "PNG")
            shadow.save(shadow_mask_path, "PNG")
    except ValueError as exc:
        sys.exit(str(exc))

    json.dump(
        {
            "output": str(output_path),
            "product_layer": str(product_layer_path),
            "shadow_mask": str(shadow_mask_path),
            "product_box": {"left": left, "top": top, "right": right, "bottom": bottom},
            "placement": {
                "profile": profile,
                "source_aspect": round(source_aspect, 4),
                "max_width_frac": max_width_frac,
                "bottom_margin_frac": bottom_margin_frac,
            },
            "shadow": {
                "angle_degrees": ANGLE_DEGREES,
                "offset_x": offset_x,
                "offset_y": offset_y,
                "blur_radius": blur,
                "opacity": SHADOW_OPACITY,
            },
        },
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )
    print()


if __name__ == "__main__":
    main()
