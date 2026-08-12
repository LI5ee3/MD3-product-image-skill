#!/usr/bin/env python3
"""Apply a prepared md3-product-image information group to an accepted scene."""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter, ImageStat


MIN_TEXT_BACKGROUND_CONTRAST = 3.0
MIN_LOGO_BACKGROUND_CONTRAST = 1.5
VERSION_CONTRAST_FACTOR = 0.95
AUTO_COLOR_LEVELS = (0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 255)
OUTPUT_KINDS = ("CANDIDATE", "ORIGINAL_MASTER_FINAL", "SKU_VARIANT")


def parse_color(value: str) -> tuple[int, int, int]:
    raw = value.lstrip("#")
    if len(raw) != 6:
        raise ValueError(f"INVALID_COLOR: {value!r} must be RRGGBB")
    try:
        return tuple(int(raw[index : index + 2], 16) for index in (0, 2, 4))
    except ValueError as exc:
        raise ValueError(f"INVALID_COLOR: {value!r} must be RRGGBB") from exc


def load_image(path: Path, mode: str) -> Image.Image:
    try:
        with Image.open(path) as source:
            image = source.convert(mode)
            image.load()
            return image
    except OSError as exc:
        raise ValueError(f"ASSET_UNREADABLE: {path}: {exc}") from exc


def target_box(rect: dict, width: int, height: int) -> tuple[int, int, int, int]:
    left = round(rect["x"] * width)
    top = round(rect["y"] * height)
    target_width = max(1, round(rect["w"] * width))
    target_height = max(1, round(rect["h"] * height))
    return left, top, target_width, target_height


def relative_luminance(color: tuple[int, int, int]) -> float:
    def linearize(channel: int) -> float:
        value = channel / 255
        return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4

    red, green, blue = (linearize(channel) for channel in color)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(first: tuple[int, int, int], second: tuple[int, int, int]) -> float:
    lighter, darker = sorted((relative_luminance(first), relative_luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def color_hex(color: tuple[int, int, int]) -> str:
    return "".join(f"{channel:02X}" for channel in color)


def minimum_contrast(
    color: tuple[int, int, int], backgrounds: list[tuple[int, int, int]]
) -> float:
    return min(contrast_ratio(color, background) for background in backgrounds)


def choose_neutral_color(
    backgrounds: list[tuple[int, int, int]],
    target_contrast: float,
    minimum: float,
    upper_contrast: float | None = None,
) -> tuple[int, int, int]:
    choices = []
    for level in AUTO_COLOR_LEVELS:
        color = (level, level, level)
        contrast = minimum_contrast(color, backgrounds)
        if contrast < minimum:
            continue
        if upper_contrast is not None and contrast >= upper_contrast:
            continue
        choices.append((abs(contrast - target_contrast), -contrast, color))
    if not choices:
        raise ValueError("NO_READABLE_INFORMATION_COLOR")
    return min(choices, key=lambda item: (item[0], item[1]))[2]


def background_color_under_mask(
    scene: Image.Image,
    asset_path: Path,
    rect: dict,
    width: int,
    height: int,
) -> tuple[int, int, int]:
    left, top, target_width, target_height = target_box(rect, width, height)
    if left < 0 or top < 0 or left + target_width > width or top + target_height > height:
        raise ValueError("VERSION_TEXT_RECT_OUTSIDE_CANVAS")
    mask = load_image(asset_path, "L").resize(
        (target_width, target_height), Image.Resampling.LANCZOS
    )
    if mask.getbbox() is None:
        raise ValueError("VERSION_MASK_EMPTY")
    background = scene.crop(
        (left, top, left + target_width, top + target_height)
    ).convert("RGB")
    return tuple(int(value) for value in ImageStat.Stat(background, mask).median)


def logo_background_contrast(
    scene: Image.Image,
    asset_path: Path,
    rect: dict,
    width: int,
    height: int,
) -> float:
    left, top, target_width, target_height = target_box(rect, width, height)
    if left < 0 or top < 0 or left + target_width > width or top + target_height > height:
        raise ValueError("LOGO_RECT_OUTSIDE_CANVAS")
    logo = load_image(asset_path, "RGBA").resize(
        (target_width, target_height), Image.Resampling.LANCZOS
    )
    alpha = logo.getchannel("A")
    if alpha.getbbox() is None:
        raise ValueError("LOGO_EMPTY")
    edge_depth = max(1, round(min(target_width, target_height) * 0.05))
    filter_size = edge_depth * 2 + 1
    edge = ImageChops.subtract(alpha, alpha.filter(ImageFilter.MinFilter(filter_size)))
    if edge.getbbox() is None:
        edge = alpha
    background = scene.crop(
        (left, top, left + target_width, top + target_height)
    ).convert("RGB")
    logo_color = tuple(
        int(value) for value in ImageStat.Stat(logo.convert("RGB"), edge).median
    )
    background_color = tuple(
        int(value) for value in ImageStat.Stat(background, edge).median
    )
    return contrast_ratio(logo_color, background_color)


def resolve_information_colors(
    scene: Image.Image,
    base: Path,
    title_rects: list[dict],
    version_rect: dict | None,
    width: int,
    height: int,
    supplied_title: tuple[int, int, int] | None,
    supplied_version: tuple[int, int, int] | None,
) -> tuple[tuple[int, int, int], tuple[int, int, int] | None]:
    title_backgrounds = [
        background_color_under_mask(
            scene, base / rect["asset"], rect, width, height
        )
        for rect in title_rects
    ]
    title_color = supplied_title or choose_neutral_color(
        title_backgrounds, target_contrast=7.0, minimum=MIN_TEXT_BACKGROUND_CONTRAST
    )
    title_contrast = minimum_contrast(title_color, title_backgrounds)
    if title_contrast < MIN_TEXT_BACKGROUND_CONTRAST:
        raise ValueError(
            f"TITLE_COLOR_BACKGROUND_CONTRAST_TOO_LOW: {title_contrast:.2f} "
            f"< {MIN_TEXT_BACKGROUND_CONTRAST:.2f}"
        )

    if version_rect is None:
        if supplied_version is not None:
            raise ValueError("VERSION_COLOR_NOT_APPLICABLE")
        return title_color, None

    version_backgrounds = [
        background_color_under_mask(
            scene,
            base / version_rect["asset"],
            version_rect,
            width,
            height,
        )
    ]
    version_color = supplied_version or choose_neutral_color(
        version_backgrounds,
        target_contrast=max(MIN_TEXT_BACKGROUND_CONTRAST, title_contrast * 0.72),
        minimum=MIN_TEXT_BACKGROUND_CONTRAST,
        upper_contrast=title_contrast * VERSION_CONTRAST_FACTOR,
    )
    version_contrast = minimum_contrast(version_color, version_backgrounds)
    if version_contrast < MIN_TEXT_BACKGROUND_CONTRAST:
        raise ValueError(
            f"VERSION_COLOR_BACKGROUND_CONTRAST_TOO_LOW: {version_contrast:.2f} "
            f"< {MIN_TEXT_BACKGROUND_CONTRAST:.2f}"
        )
    if version_contrast >= title_contrast:
        raise ValueError(
            "VERSION_COLOR_TOO_PROMINENT: version contrast must be lower than title"
        )
    return title_color, version_color


def paste_logo(
    scene: Image.Image, asset_path: Path, rect: dict, width: int, height: int
) -> None:
    left, top, target_width, target_height = target_box(rect, width, height)
    logo = load_image(asset_path, "RGBA").resize(
        (target_width, target_height), Image.Resampling.LANCZOS
    )
    scene.paste(logo, (left, top), logo)


def paste_text_mask(
    scene: Image.Image,
    asset_path: Path,
    rect: dict,
    color: tuple[int, int, int],
    width: int,
    height: int,
) -> None:
    left, top, target_width, target_height = target_box(rect, width, height)
    mask = load_image(asset_path, "L").resize(
        (target_width, target_height), Image.Resampling.LANCZOS
    )
    layer = Image.new("RGBA", mask.size, color + (255,))
    layer.putalpha(mask)
    scene.paste(layer, (left, top), layer)


def validate_output_path(kind: str, output: Path, product_dir: Path) -> None:
    if kind == "CANDIDATE":
        if (
            output.parent != product_dir
            or not output.name.startswith("master-candidate-")
            or output.name == "master-candidate-.png"
            or output.suffix.lower() != ".png"
            or output.name.endswith(("-scene.png", "-thumb.png"))
        ):
            raise ValueError(
                "CANDIDATE_PATH_INVALID: expected product/master-candidate-<id>.png"
            )
        return

    output_dir = product_dir / "output"
    output_dir.mkdir(exist_ok=True)
    if kind == "ORIGINAL_MASTER_FINAL":
        expected = output_dir / "ORIGINAL_MASTER_FINAL.png"
        if output != expected:
            raise ValueError(f"MASTER_FINAL_PATH_INVALID: expected {expected}")
        return

    if (
        output.parent != output_dir
        or not output.name.startswith("SKU_VARIANT-")
        or output.name == "SKU_VARIANT-.png"
        or output.suffix.lower() != ".png"
    ):
        raise ValueError(
            "SKU_FINAL_PATH_INVALID: expected output/SKU_VARIANT-<label>.png"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene", required=True)
    parser.add_argument("--layout", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--output-kind", required=True, choices=OUTPUT_KINDS)
    parser.add_argument("--text-color", default=None)
    parser.add_argument("--version-color", default=None)
    args = parser.parse_args()

    scene_path = Path(args.scene).expanduser().resolve()
    layout_path = Path(args.layout).expanduser().resolve()
    try:
        scene = load_image(scene_path, "RGBA")
        with layout_path.open(encoding="utf-8") as handle:
            layout = json.load(handle)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        sys.exit(str(exc))

    width, height = scene.size
    if width * 4 != height * 3:
        sys.exit(f"SCENE_NOT_3_4: got {width}x{height}")
    if layout.get("canvas", {}).get("ratio") != "3:4":
        sys.exit("LAYOUT_NOT_3_4")

    product_dir = layout_path.parent
    if layout_path.name != "layout.json":
        sys.exit("LAYOUT_PATH_INVALID: expected <complete product name>/layout.json")
    if layout.get("product_directory") != str(product_dir):
        sys.exit("PRODUCT_DIRECTORY_MISMATCH")
    if scene_path.parent != product_dir:
        sys.exit("SCENE_OUTSIDE_PRODUCT_DIRECTORY")
    output = Path(args.output).expanduser().resolve()
    try:
        validate_output_path(args.output_kind, output, product_dir)
    except ValueError as exc:
        sys.exit(str(exc))
    if output.exists():
        sys.exit(f"REFUSE_OVERWRITE: {output}")

    base = layout_path.parent
    try:
        elements = layout["elements"]
        logo_rect = elements["LOGO_RECT"]
        title_rects = elements["TITLE_LINE_RECT"]
        version_rect = elements.get("VERSION_TEXT_RECT")
    except (KeyError, TypeError) as exc:
        sys.exit(f"LAYOUT_INVALID: {exc}")

    try:
        logo_contrast = logo_background_contrast(
            scene, base / logo_rect["asset"], logo_rect, width, height
        )
        if logo_contrast < MIN_LOGO_BACKGROUND_CONTRAST:
            raise ValueError(
                f"LOGO_BACKGROUND_CONTRAST_TOO_LOW: {logo_contrast:.2f} "
                f"< {MIN_LOGO_BACKGROUND_CONTRAST:.2f}"
            )
        supplied_title = parse_color(args.text_color) if args.text_color else None
        supplied_version = (
            parse_color(args.version_color) if args.version_color else None
        )
        title_color, version_color = resolve_information_colors(
            scene,
            base,
            title_rects,
            version_rect,
            width,
            height,
            supplied_title,
            supplied_version,
        )
    except (KeyError, TypeError) as exc:
        sys.exit(f"LAYOUT_INVALID: {exc}")
    except ValueError as exc:
        sys.exit(str(exc))

    try:
        paste_logo(scene, base / logo_rect["asset"], logo_rect, width, height)
        for title_rect in title_rects:
            paste_text_mask(
                scene,
                base / title_rect["asset"],
                title_rect,
                title_color,
                width,
                height,
            )
        if version_rect:
            paste_text_mask(
                scene,
                base / version_rect["asset"],
                version_rect,
                version_color,
                width,
                height,
            )
    except (KeyError, TypeError, ValueError) as exc:
        sys.exit(f"LAYOUT_INVALID: {exc}")

    scene.convert("RGB").save(output, "PNG")
    json.dump(
        {
            "output": str(output),
            "scene": str(scene_path),
            "layout": str(layout_path),
            "output_kind": args.output_kind,
            "rendered_title": layout.get("rendered_title"),
            "title_lines": layout.get("title_lines"),
            "logo_background_contrast": round(logo_contrast, 3),
            "title_color": color_hex(title_color),
            "version_color": color_hex(version_color) if version_color else None,
        },
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )
    print()


if __name__ == "__main__":
    main()
