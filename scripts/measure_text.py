#!/usr/bin/env python3
"""Prepare one reusable information-group layout for md3-product-image."""

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_DEFAULT = Path(__file__).resolve().parent.parent / "assets" / "Roboto-Bold.ttf"


def mask_signature(font: ImageFont.FreeTypeFont, text: str) -> tuple:
    mask = font.getmask(text, mode="L")
    return mask.size, mask.getbbox(), bytes(mask)


def check_glyph_coverage(font_path: Path, *texts: str) -> None:
    """Reject characters rendered as the font's missing-glyph box."""
    font = ImageFont.truetype(str(font_path), 96)
    missing = mask_signature(font, "\U0010ffff")
    absent = sorted(
        {
            ch
            for text in texts
            for ch in text
            if not ch.isspace() and mask_signature(font, ch) == missing
        }
    )
    if absent:
        raise ValueError(
            f"GLYPH_MISSING: {font_path} cannot render: {''.join(absent)}"
        )


def render_text_mask(font: ImageFont.FreeTypeFont, text: str) -> Image.Image:
    bbox = font.getbbox(text)
    width = max(1, bbox[2] - bbox[0])
    height = max(1, bbox[3] - bbox[1])
    probe = Image.new("L", (width + 16, height + 16), 0)
    ImageDraw.Draw(probe).text(
        (8 - bbox[0], 8 - bbox[1]), text, font=font, fill=255
    )
    ink = probe.getbbox()
    if ink is None:
        raise ValueError(f"TEXT_EMPTY: {text!r} has no visible glyphs")
    return probe.crop(ink)


def font_for_lines_height(
    font_path: Path, lines: list[str], target_height: int
) -> ImageFont.FreeTypeFont:
    lo, hi = 1, max(16, target_height * 4)
    candidates: list[tuple[int, int, ImageFont.FreeTypeFont]] = []
    while lo <= hi:
        size = (lo + hi) // 2
        font = ImageFont.truetype(str(font_path), size)
        height = max(render_text_mask(font, line).height for line in lines)
        candidates.append((abs(height - target_height), size, font))
        if height < target_height:
            lo = size + 1
        elif height > target_height:
            hi = size - 1
        else:
            hi = size - 1
    return min(candidates, key=lambda item: (item[0], item[1]))[2]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise ValueError(f"ASSET_UNREADABLE: {path}: {exc}") from exc
    return digest.hexdigest()


def image_metadata(image_path: Path) -> dict:
    try:
        with Image.open(image_path) as source:
            source.load()
            width, height = source.size
            mode = source.mode
            image_format = source.format
            alpha = source.convert("RGBA").getchannel("A")
    except OSError as exc:
        raise ValueError(f"PRODUCT_REFERENCE_UNREADABLE: {exc}") from exc
    if image_format != "PNG" or alpha.getextrema() == (255, 255):
        raise ValueError("PRODUCT_TRANSPARENT_PNG_REQUIRED")
    visible_bbox = alpha.point(lambda value: 255 if value >= 224 else 0).getbbox()
    if visible_bbox is None:
        raise ValueError("PRODUCT_ALPHA_EMPTY")
    return {
        "path": str(image_path),
        "sha256": sha256_file(image_path),
        "width": width,
        "height": height,
        "mode": mode,
        "format": image_format,
        "ratio_exact_3_4": width * 4 == height * 3,
        "visible_bbox": {
            "left": visible_bbox[0],
            "top": visible_bbox[1],
            "right": visible_bbox[2],
            "bottom": visible_bbox[3],
        },
    }


def visible_logo(logo_path: Path) -> tuple[Image.Image, dict]:
    try:
        with Image.open(logo_path) as source:
            source.load()
            source_width, source_height = source.size
            source_mode = source.mode
            source_format = source.format
            logo = source.convert("RGBA")
    except OSError as exc:
        raise ValueError(f"LOGO_UNREADABLE: {exc}") from exc
    bbox = logo.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError(f"LOGO_EMPTY: no visible artwork in {logo_path}")
    cropped = logo.crop(bbox)
    return cropped, {
        "source_path": str(logo_path),
        "sha256": sha256_file(logo_path),
        "source_width": source_width,
        "source_height": source_height,
        "source_mode": source_mode,
        "source_format": source_format,
        "visible_bbox": {
            "left": bbox[0],
            "top": bbox[1],
            "right": bbox[2],
            "bottom": bbox[3],
        },
        "cropped_width": cropped.width,
        "cropped_height": cropped.height,
        "cropped_asset": "logo.png",
    }


def resolve_product_directory(output_root: Path, complete_name: str) -> Path:
    if (
        not complete_name
        or complete_name in {".", ".."}
        or "/" in complete_name
        or "\x00" in complete_name
    ):
        raise ValueError(
            "PRODUCT_FOLDER_NAME_INVALID: complete name must be one exact folder name"
        )
    root = output_root.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    candidate = root / complete_name
    candidate.mkdir(exist_ok=True)
    product_dir = candidate.resolve()
    if product_dir.parent != root or product_dir.name != complete_name:
        raise ValueError("PRODUCT_FOLDER_OUTSIDE_ROOT")
    (product_dir / "output").mkdir(exist_ok=True)
    return product_dir


@dataclass
class LayoutOptions:
    title_height_frac: float = 0.045
    version_height_frac: float = 0.0285
    logo_height_frac: float = 0.073
    logo_width_cap_frac: float = 0.30
    left_margin_frac: float = 0.05
    top_margin_frac: float = 0.05
    title_top_frac: float = 0.18
    title_version_gap_frac: float = 0.025
    clearance_w_frac: float = 0.02
    clearance_h_frac: float = 0.015
    max_title_width_frac: float = 0.90
    line_gap_factor: float = 0.45
    font_path: Path = field(default_factory=lambda: FONT_DEFAULT)


def natural_two_line_split(
    text: str, font: ImageFont.FreeTypeFont
) -> list[str]:
    candidates = []
    for index, char in enumerate(text):
        if char != " ":
            continue
        first, second = text[:index], text[index + 1 :]
        if not first or not second:
            continue
        widths = (render_text_mask(font, first).width, render_text_mask(font, second).width)
        candidates.append((max(widths), abs(widths[0] - widths[1]), first, second))
    if not candidates:
        raise ValueError("TEXT_LOGO_TITLE_SPLIT_UNAVAILABLE: no natural word boundary")
    _, _, first, second = min(candidates)
    return [first, second]


def resolve_title_lines(
    complete_name: str,
    brand: str,
    remaining_name: str,
    logo_type: str,
    title_line_count: int,
    canvas_width: int,
    canvas_height: int,
    opts: LayoutOptions,
) -> tuple[str, list[str], ImageFont.FreeTypeFont]:
    expected_complete = f"{brand} {remaining_name}" if remaining_name else brand
    if complete_name != expected_complete:
        raise ValueError(
            "PRODUCT_NAME_MISMATCH: complete name must equal brand + one space + remaining name"
        )

    rendered_title = remaining_name if logo_type == "TEXT" else complete_name
    if not rendered_title:
        raise ValueError("TITLE_EMPTY: rendered title is empty")

    target_height = round(opts.title_height_frac * canvas_height)
    if title_line_count == 1:
        lines = [rendered_title]
    elif logo_type == "GRAPHIC":
        if not brand or not remaining_name:
            raise ValueError("TITLE_WRAP_INVALID: brand and remaining name are required")
        lines = [brand, remaining_name]
    else:
        split_font = font_for_lines_height(
            opts.font_path, [rendered_title], target_height
        )
        lines = natural_two_line_split(rendered_title, split_font)

    if len(lines) != title_line_count or any(not line for line in lines):
        raise ValueError("TITLE_LINE_COUNT_MISMATCH")
    if " ".join(lines) != rendered_title:
        raise ValueError("TITLE_WRAP_MISMATCH: wrapped lines change the exact title")

    title_font = font_for_lines_height(opts.font_path, lines, target_height)
    if any(
        render_text_mask(title_font, line).width
        > opts.max_title_width_frac * canvas_width
        for line in lines
    ):
        raise ValueError("TITLE_LINE_OVERFLOW: user-selected line count does not fit")
    return rendered_title, lines, title_font


def normalized_rect(rect: tuple[float, float, float, float], width: int, height: int) -> dict:
    left, top, right, bottom = rect
    return {
        "x": round(left / width, 6),
        "y": round(top / height, 6),
        "w": round((right - left) / width, 6),
        "h": round((bottom - top) / height, 6),
    }


def clear_zones(
    labeled_rects: list[tuple[str, tuple[float, float, float, float]]],
    width: int,
    height: int,
    opts: LayoutOptions,
) -> list[dict]:
    pad_w = opts.clearance_w_frac * width
    pad_h = opts.clearance_h_frac * height
    padded = [
        (
            label,
            (rect[0] - pad_w, rect[1] - pad_h, rect[2] + pad_w, rect[3] + pad_h),
        )
        for label, rect in labeled_rects
    ]
    zones = []
    for label, rect in padded:
        zones.append({"label": label, **normalized_rect(rect, width, height)})
    for (_, upper), (_, lower) in zip(padded, padded[1:]):
        left = max(upper[0], lower[0])
        right = min(upper[2], lower[2])
        top, bottom = upper[3], lower[1]
        if bottom > top and right > left:
            zones.append(
                {
                    "label": "CONNECTOR",
                    **normalized_rect((left, top, right, bottom), width, height),
                }
            )
    for zone in zones:
        if (
            zone["x"] < 0
            or zone["y"] < 0
            or zone["x"] + zone["w"] > 1
            or zone["y"] + zone["h"] > 1
        ):
            raise ValueError(f"CLEAR_ZONE_OUT_OF_CANVAS: {zone['label']}")
    return zones


def prepare_layout(args: argparse.Namespace) -> dict:
    opts = LayoutOptions(font_path=Path(args.font_path))
    if not opts.font_path.is_file():
        raise FileNotFoundError(f"FONT_UNAVAILABLE: {opts.font_path}")
    if args.canvas_height <= 0 or args.canvas_height % 4:
        raise ValueError("CANVAS_HEIGHT_INVALID: use a positive multiple of 4")

    width, height = args.canvas_height * 3 // 4, args.canvas_height
    check_glyph_coverage(
        opts.font_path,
        args.complete_name,
        args.brand,
        args.remaining_name,
        args.version or "",
    )
    rendered_title, title_lines, title_font = resolve_title_lines(
        args.complete_name,
        args.brand,
        args.remaining_name,
        args.logo_type,
        args.title_lines,
        width,
        height,
        opts,
    )

    product_reference = Path(args.product_reference).expanduser().resolve()
    logo_path = Path(args.logo).expanduser().resolve()
    product_metadata = image_metadata(product_reference)
    output_dir = resolve_product_directory(Path(args.output_root), args.complete_name)
    layout_path = output_dir / "layout.json"
    if layout_path.exists():
        raise ValueError(f"REFUSE_REMEASURE: reuse existing {layout_path}")
    logo_art, logo_metadata = visible_logo(logo_path)
    logo_art.save(output_dir / "logo.png")

    x0 = opts.left_margin_frac * width
    logo_height = opts.logo_height_frac * height
    logo_width = logo_art.width * logo_height / logo_art.height
    if logo_width > opts.logo_width_cap_frac * width:
        scale = opts.logo_width_cap_frac * width / logo_width
        logo_width *= scale
        logo_height *= scale
    logo_rect = (
        x0,
        opts.top_margin_frac * height,
        x0 + logo_width,
        opts.top_margin_frac * height + logo_height,
    )

    title_masks = [render_text_mask(title_font, line) for line in title_lines]
    title_top = max(opts.title_top_frac * height, logo_rect[3] + 0.02 * height)
    title_rects = []
    for index, (line, mask) in enumerate(zip(title_lines, title_masks), start=1):
        mask_path = output_dir / f"title-{index}-mask.png"
        mask.save(mask_path)
        rect = (x0, title_top, x0 + mask.width, title_top + mask.height)
        title_rects.append((line, rect, mask_path.name))
        title_top += mask.height * (1 + opts.line_gap_factor)

    version_rect = None
    version_asset = None
    version_font_size = None
    if args.version:
        version_font = font_for_lines_height(
            opts.font_path,
            [args.version],
            round(opts.version_height_frac * height),
        )
        version_mask = render_text_mask(version_font, args.version)
        version_asset = "version-mask.png"
        version_mask.save(output_dir / version_asset)
        gap = opts.title_version_gap_frac * height
        top = title_rects[-1][1][3] + gap
        version_rect = (x0, top, x0 + version_mask.width, top + version_mask.height)
        version_font_size = version_font.size

    labeled_rects = [("LOGO_RECT", logo_rect)]
    labeled_rects.extend(
        (f"TITLE_LINE_RECT_{index}", rect)
        for index, (_, rect, _) in enumerate(title_rects, start=1)
    )
    if version_rect:
        labeled_rects.append(("VERSION_TEXT_RECT", version_rect))

    elements = {
        "LOGO_RECT": {**normalized_rect(logo_rect, width, height), "asset": "logo.png"},
        "TITLE_LINE_RECT": [
            {
                "line": line,
                **normalized_rect(rect, width, height),
                "asset": asset,
            }
            for line, rect, asset in title_rects
        ],
        "TITLE_FONT_SIZE": title_font.size,
    }
    if version_rect:
        elements["VERSION_TEXT_RECT"] = {
            "text": args.version,
            **normalized_rect(version_rect, width, height),
            "asset": version_asset,
        }
        elements["VERSION_FONT_SIZE"] = version_font_size

    information_assets = {
        "logo": {
            "path": "logo.png",
            "sha256": sha256_file(output_dir / "logo.png"),
        }
    }
    for index, (_, _, asset) in enumerate(title_rects, start=1):
        information_assets[f"title_{index}"] = {
            "path": asset,
            "sha256": sha256_file(output_dir / asset),
        }
    if version_asset:
        information_assets["version"] = {
            "path": version_asset,
            "sha256": sha256_file(output_dir / version_asset),
        }

    report = {
        "product_directory": str(output_dir),
        "canvas": {
            "width": width,
            "height": height,
            "ratio": "3:4",
            "purpose": "logical layout only",
        },
        "font": {"path": str(opts.font_path), "name": "Roboto Bold"},
        "product_reference": product_metadata,
        "logo": logo_metadata,
        "logo_type": args.logo_type,
        "title_line_count": args.title_lines,
        "complete_name": args.complete_name,
        "brand": args.brand,
        "remaining_name": args.remaining_name,
        "rendered_title": rendered_title,
        "title_lines": title_lines,
        "version": args.version,
        "elements": elements,
        "information_assets": information_assets,
        "clear_zones": clear_zones(labeled_rects, width, height, opts),
    }
    temporary = output_dir / ".layout.json.tmp"
    temporary_created = False
    try:
        with temporary.open("x", encoding="utf-8") as handle:
            temporary_created = True
            json.dump(report, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        temporary.replace(layout_path)
    except Exception:
        if temporary_created and temporary.exists():
            temporary.unlink()
        raise
    attempt_state_path = output_dir / "scene-attempts.json"
    attempt_state_temporary = output_dir / ".scene-attempts.json.tmp"
    attempt_state_created = False
    try:
        with attempt_state_temporary.open("x", encoding="utf-8") as handle:
            attempt_state_created = True
            json.dump(
                {"schema": 1, "next_run": 1, "active_run_id": None, "runs": []},
                handle,
                ensure_ascii=False,
                indent=2,
            )
            handle.write("\n")
        attempt_state_temporary.replace(attempt_state_path)
    except Exception:
        if attempt_state_created and attempt_state_temporary.exists():
            attempt_state_temporary.unlink()
        raise
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--complete-name", required=True)
    parser.add_argument("--brand", required=True)
    parser.add_argument("--remaining-name", required=True)
    parser.add_argument(
        "--logo-type",
        required=True,
        choices=("GRAPHIC", "TEXT"),
    )
    parser.add_argument("--title-lines", required=True, type=int, choices=(1, 2))
    parser.add_argument("--version", default=None)
    parser.add_argument("--product-reference", required=True)
    parser.add_argument("--logo", required=True)
    parser.add_argument(
        "--output-root",
        required=True,
        help="parent directory; the exact complete product name is appended automatically",
    )
    parser.add_argument("--canvas-height", type=int, default=2048)
    parser.add_argument("--font-path", default=str(FONT_DEFAULT))
    args = parser.parse_args()

    try:
        report = prepare_layout(args)
    except (FileNotFoundError, ValueError) as exc:
        sys.exit(str(exc))
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
