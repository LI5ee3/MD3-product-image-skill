#!/usr/bin/env python3
"""Compose the exact information group onto an accepted scene for md3-product-image.

Per SKILL.md ("Add the exact information group"), only the original Logo and the
exact typography are added after scene acceptance: the Logo as one flat asset,
the title and version rendered from the bundled Roboto Bold, all placed at the
exact rectangles computed by `measure_text.py`. Rendering and measurement share
`compute_layout()`, so the composited glyphs land exactly inside the measured
and protected clear zones.

The scene must be an exact portrait 3:4 canvas. Nothing else in the scene is
modified, and no backing, effect, or re-render is applied to the information.

Usage:
  python scripts/compose_image.py --scene scene.png --output final.png \\
      --title "Product Name" [--title-lines "Line One|Line Two"] \\
      [--version "Version Text"] [--logo logo.png]

Optional overrides (mirror measure_text.py):
  --title-height-frac, --version-height-frac, --logo-height-frac,
  --logo-width-cap-frac, --left-margin-frac, --top-margin-frac,
  --title-top-frac, --title-gap-factor, --two-line-title-gap, --font-path
  --text-color RRGGBB       solid title color (default 000000)
  --version-color RRGGBB    solid version color (default = --text-color)
"""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from measure_text import FONT_DEFAULT, LayoutOptions, compute_layout, layout_report


def render_text_layer(
    font: ImageFont.FreeTypeFont, text: str, color: tuple[int, int, int]
) -> Image.Image:
    """Render `text` and return the ink-cropped layer.

    The glyphs are drawn at the origin of a temporary canvas and cropped to the
    ink bounding box, which matches the ink box measured by `measure_text.py`
    (anchor offset cancels out), so the layer pastes exactly inside the planned
    content rectangle.
    """
    mask = font.getmask(text)
    probe = Image.new("L", (mask.size[0] + 64, mask.size[1] + 64), 0)
    ImageDraw.Draw(probe).text((0, 0), text, font=font, fill=255)
    bbox = probe.getbbox()
    raw = probe.crop(bbox)
    layer = Image.new("RGBA", raw.size, color + (255,))
    layer.putalpha(raw)
    return layer


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--title-lines", default=None, help="force two lines, '|' separated")
    parser.add_argument("--version", default=None)
    parser.add_argument("--logo", default=None)
    parser.add_argument("--title-height-frac", type=float, default=LayoutOptions.title_height_frac)
    parser.add_argument("--version-height-frac", type=float, default=LayoutOptions.version_height_frac)
    parser.add_argument("--logo-height-frac", type=float, default=LayoutOptions.logo_height_frac)
    parser.add_argument("--logo-width-cap-frac", type=float, default=LayoutOptions.logo_width_cap_frac)
    parser.add_argument("--left-margin-frac", type=float, default=LayoutOptions.left_margin_frac)
    parser.add_argument("--top-margin-frac", type=float, default=LayoutOptions.top_margin_frac)
    parser.add_argument("--title-top-frac", type=float, default=LayoutOptions.title_top_frac)
    parser.add_argument("--title-gap-factor", type=float, default=LayoutOptions.title_gap_factor)
    parser.add_argument("--two-line-title-gap", type=float, default=LayoutOptions.two_line_title_gap)
    parser.add_argument("--font-path", default=str(FONT_DEFAULT))
    parser.add_argument("--text-color", default="000000", help="solid title color as RRGGBB")
    parser.add_argument("--version-color", default=None, help="solid version color as RRGGBB; defaults to --text-color")
    args = parser.parse_args()

    def parse_color(value: str) -> tuple[int, int, int]:
        value = value.lstrip("#")
        if len(value) != 6:
            raise SystemExit(f"INVALID_COLOR: {value!r} must be RRGGBB")
        return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))

    try:
        scene = Image.open(args.scene)
        scene.load()
    except OSError as exc:
        sys.exit(f"SCENE_UNREADABLE: {exc}")
    scene = scene.convert("RGBA")

    w, h = scene.size
    if w * 4 != h * 3:
        sys.exit(f"SCENE_NOT_3_4: got {w}x{h}")

    title_lines = args.title_lines.split("|") if args.title_lines else [args.title]
    opts = LayoutOptions(
        title_height_frac=args.title_height_frac,
        version_height_frac=args.version_height_frac,
        logo_height_frac=args.logo_height_frac,
        logo_width_cap_frac=args.logo_width_cap_frac,
        left_margin_frac=args.left_margin_frac,
        top_margin_frac=args.top_margin_frac,
        title_top_frac=args.title_top_frac,
        title_gap_factor=args.title_gap_factor,
        two_line_title_gap=args.two_line_title_gap,
        font_path=Path(args.font_path),
    )

    try:
        layout = compute_layout(
            h, title_lines, args.version, Path(args.logo) if args.logo else None, opts
        )
    except (FileNotFoundError, ValueError) as exc:
        sys.exit(str(exc))

    title_color = parse_color(args.text_color)
    version_color = parse_color(args.version_color) if args.version_color else title_color

    if args.logo and layout.logo_rect is not None and layout.logo_bbox is not None:
        art = Image.open(args.logo).convert("RGBA")
        bx0, by0, bx1, by1 = layout.logo_bbox
        art = art.crop((bx0, by0, bx1, by1))
        lx, ly, rx, ry = layout.logo_rect
        art = art.resize((max(1, round(rx - lx)), max(1, round(ry - ly))), Image.LANCZOS)
        scene.paste(art, (round(lx), round(ly)), art)

    for rect, line in layout.title_line_rects:
        layer = render_text_layer(layout.title_font, line, title_color)
        scene.paste(layer, (round(rect[0]), round(rect[1])), layer)

    if layout.version_rect is not None and layout.version_font is not None:
        layer = render_text_layer(layout.version_font, args.version, version_color)
        scene.paste(layer, (round(layout.version_rect[0]), round(layout.version_rect[1])), layer)

    scene.convert("RGB").save(args.output, "PNG")
    report = layout_report(layout, opts)
    report["output"] = str(args.output)
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
