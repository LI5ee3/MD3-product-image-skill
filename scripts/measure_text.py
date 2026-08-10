#!/usr/bin/env python3
"""Measure exact visible glyph bounds and Logo artwork for the md3-product-image skill.

Reads the bundled Roboto Bold font and an optional transparent Logo PNG, then
emits the normalized (fractions of canvas width/height) content rectangles
LOGO_RECT, TITLE_LINE_RECT(s), VERSION_TEXT_RECT plus the connected stepped
INFORMATION_CLEAR_ZONES, per SKILL.md ("Run preflight and measure text").

The canvas is a strict portrait 3:4; only the height is configurable.

Usage:
  python scripts/measure_text.py --canvas-height 1024 \\
      --title "Product Name" [--title-lines "Line One|Line Two"] \\
      [--version "Version Text"] [--logo logo.png]

Optional overrides (defaults follow SKILL.md guidance):
  --title-height-frac 0.045   visible title letter height as canvas-height fraction
  --version-height-frac 0.03  visible version letter height as canvas-height fraction
  --logo-height-frac 0.05     visible Logo height as canvas-height fraction
  --logo-width-cap-frac 0.30  maximum visible Logo width as canvas-width fraction
  --left-margin-frac 0.05     text axis / Logo left margin
  --top-margin-frac 0.05      Logo top margin
  --title-top-frac 0.18       first title line visible top
  --title-gap-factor 1.2      title-to-version gap in version letter heights
  --two-line-title-gap 0.85   same gap when the title has two lines
  --clearance-w-frac 0.02     horizontal optical clearance per row
  --clearance-h-frac 0.015    vertical optical clearance per row
  --max-title-width-frac 0.9  single-line title fit-test limit
  --font-path PATH            override the bundled font

Outputs one JSON document on stdout.

The layout computation is exposed as `compute_layout()` and shared with
`compose_image.py` so measurement and composition always agree.
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageFont
from fontTools.ttLib import TTFont

FONT_DEFAULT = Path(__file__).resolve().parent.parent / "assets" / "Roboto-Bold.ttf"


def check_glyph_coverage(font_path: Path, *texts: str) -> None:
    """Raise when any character of `texts` is missing from the font cmap.

    Pillow would silently render the .notdef box, breaking character-exact
    fidelity; stop instead per SKILL.md preflight rules.
    """
    cmap = TTFont(str(font_path)).getBestCmap()
    missing = sorted(
        {ch for text in texts for ch in set(text) if ord(ch) not in cmap}
    )
    if missing:
        raise ValueError(
            f"GLYPH_MISSING: {font_path} cannot render: {''.join(missing)}"
        )


def visible_text_bounds(font: ImageFont.FreeTypeFont, text: str) -> tuple[int, int]:
    """Return visible ink width/height of `text` at the given font size."""
    bbox = font.getmask(text).getbbox()
    if bbox is None:
        return 0, 0
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def font_for_height(font_path: Path, target_h: int) -> ImageFont.FreeTypeFont:
    """Return the font at a point size whose visible ink height hits target_h."""
    size = max(1, int(target_h * 1.5))
    font = ImageFont.truetype(str(font_path), size)
    _, ink_h = visible_text_bounds(font, "AgH")
    if ink_h > 0:
        size = max(1, int(size * target_h / ink_h))
    return ImageFont.truetype(str(font_path), size)


def visible_logo_bbox(logo_path: Path) -> tuple[int, int, int, int]:
    """Return the visible (non-transparent) artwork bounding box of the PNG Logo."""
    img = Image.open(logo_path).convert("RGBA")
    bbox = img.getchannel("A").getbbox()
    if bbox is None:
        return 0, 0, 0, 0
    return bbox


@dataclass
class LayoutOptions:
    title_height_frac: float = 0.045
    version_height_frac: float = 0.03
    logo_height_frac: float = 0.05
    logo_width_cap_frac: float = 0.30
    left_margin_frac: float = 0.05
    top_margin_frac: float = 0.05
    title_top_frac: float = 0.18
    title_gap_factor: float = 1.2
    two_line_title_gap: float = 0.85
    clearance_w_frac: float = 0.02
    clearance_h_frac: float = 0.015
    max_title_width_frac: float = 0.9
    font_path: Path = field(default_factory=lambda: FONT_DEFAULT)
    line_gap_factor: float = 0.45


@dataclass
class Layout:
    W: int
    H: int
    title_lines: list[str]
    version: str | None
    logo_rect: tuple[float, float, float, float] | None
    logo_bbox: tuple[int, int, int, int] | None
    title_line_rects: list[tuple[tuple[float, float, float, float], str]]
    version_rect: tuple[float, float, float, float] | None
    title_font: ImageFont.FreeTypeFont
    version_font: ImageFont.FreeTypeFont | None
    fits_one_line: bool | None

    @property
    def title_last_rect(self) -> tuple[float, float, float, float]:
        return self.title_line_rects[-1][0]


def compute_layout(
    canvas_height: int,
    title_lines: list[str],
    version: str | None,
    logo_path: Path | None,
    opts: LayoutOptions | None = None,
) -> Layout:
    """Compute pixel-space layout for the information group on a 3:4 canvas."""
    opts = opts or LayoutOptions()
    font_path = opts.font_path
    if not font_path.is_file():
        raise FileNotFoundError(f"FONT_UNAVAILABLE: {font_path}")
    check_glyph_coverage(font_path, *title_lines, version or "")

    H = canvas_height
    W = round(H * 3 / 4)
    x0 = opts.left_margin_frac * W

    logo_rect = None
    logo_bbox = None
    if logo_path is not None:
        logo_bbox = visible_logo_bbox(logo_path)
        art_w, art_h = logo_bbox[2] - logo_bbox[0], logo_bbox[3] - logo_bbox[1]
        if art_w == 0 or art_h == 0:
            raise ValueError(f"LOGO_EMPTY: no visible artwork in {logo_path}")
        target_h = opts.logo_height_frac * H
        scale = target_h / art_h
        logo_w = art_w * scale
        width_cap = opts.logo_width_cap_frac * W
        if logo_w > width_cap:
            scale *= width_cap / logo_w
            logo_w = width_cap
            target_h = art_h * scale
        logo_y = opts.top_margin_frac * H
        logo_rect = (x0, logo_y, x0 + logo_w, logo_y + target_h)

    title_font = font_for_height(font_path, round(opts.title_height_frac * H))
    title_line_rects: list[tuple[tuple[float, float, float, float], str]] = []
    line_top = max(opts.title_top_frac * H, (logo_rect[3] + 0.02 * H) if logo_rect else 0)
    for line in title_lines:
        ink_w, ink_h = visible_text_bounds(title_font, line)
        line_rect = (x0, line_top, x0 + ink_w, line_top + ink_h)
        title_line_rects.append((line_rect, line))
        line_top += ink_h + opts.line_gap_factor * ink_h

    fits_one_line = None
    if len(title_lines) == 1:
        fit_limit = opts.max_title_width_frac * W
        first_rect = title_line_rects[0][0]
        fits_one_line = first_rect[2] - first_rect[0] <= fit_limit

    version_rect = None
    version_font = None
    if version:
        version_font = font_for_height(font_path, round(opts.version_height_frac * H))
        ink_w, ink_h = visible_text_bounds(version_font, version)
        gap_factor = opts.title_gap_factor if len(title_lines) == 1 else opts.two_line_title_gap
        version_top = title_line_rects[-1][0][3] + gap_factor * ink_h
        version_rect = (x0, version_top, x0 + ink_w, version_top + ink_h)

    return Layout(
        W=W,
        H=H,
        title_lines=title_lines,
        version=version,
        logo_rect=logo_rect,
        logo_bbox=logo_bbox,
        title_line_rects=title_line_rects,
        version_rect=version_rect,
        title_font=title_font,
        version_font=version_font,
        fits_one_line=fits_one_line,
    )


def clear_zones(layout: Layout, opts: LayoutOptions) -> list[dict]:
    """Return the connected stepped INFORMATION_CLEAR_ZONES as normalized dicts."""
    H, W = layout.H, layout.W
    pad_w = opts.clearance_w_frac * W
    pad_h = opts.clearance_h_frac * H

    labels: list[str] = []
    rects: list[tuple[float, float, float, float]] = []
    if layout.logo_rect:
        labels.append("LOGO_RECT")
        rects.append(layout.logo_rect)
    for i in range(len(layout.title_line_rects)):
        labels.append(f"TITLE_LINE_RECT_{i + 1}")
        rects.append(layout.title_line_rects[i][0])
    if layout.version_rect:
        labels.append("VERSION_TEXT_RECT")
        rects.append(layout.version_rect)

    cleared = [(r[0] - pad_w, r[1] - pad_h, r[2] + pad_w, r[3] + pad_h) for r in rects]

    def frac(x: float) -> float:
        return round(x, 6)

    zones = []
    for label, r in zip(labels, cleared):
        zones.append(
            {
                "label": label,
                "x": frac(r[0] / W),
                "y": frac(r[1] / H),
                "w": frac((r[2] - r[0]) / W),
                "h": frac((r[3] - r[1]) / H),
            }
        )
    for i in range(len(cleared) - 1):
        upper, lower = cleared[i], cleared[i + 1]
        left = max(upper[0], lower[0])
        right = min(upper[2], lower[2])
        top = upper[3]
        bottom = lower[1]
        if bottom > top and right > left:
            zones.append(
                {
                    "label": "CONNECTOR",
                    "x": frac(left / W),
                    "y": frac(top / H),
                    "w": frac((right - left) / W),
                    "h": frac((bottom - top) / H),
                }
            )
    return zones


def layout_report(layout: Layout, opts: LayoutOptions) -> dict:
    """Build the machine-readable measurement report (elements + clear zones)."""
    H, W = layout.H, layout.W

    def frac(x: float) -> float:
        return round(x, 6)

    report: dict = {
        "canvas": {"width": W, "height": H, "ratio": "3:4"},
        "font": {"path": str(opts.font_path), "name": "Roboto Bold"},
        "elements": {},
        "clear_zones": clear_zones(layout, opts),
    }

    if layout.logo_rect:
        lx, ly, rx, ry = layout.logo_rect
        report["elements"]["LOGO_RECT"] = {
            "x": frac(lx / W),
            "y": frac(ly / H),
            "w": frac((rx - lx) / W),
            "h": frac((ry - ly) / H),
            "hard_fail": frac((rx - lx) / W) > opts.logo_width_cap_frac,
        }

    report["elements"]["TITLE_LINE_RECT"] = []
    for rect, line in layout.title_line_rects:
        lx, ly, rx, ry = rect
        report["elements"]["TITLE_LINE_RECT"].append(
            {
                "line": line,
                "x": frac(lx / W),
                "y": frac(ly / H),
                "w": frac((rx - lx) / W),
                "h": frac((ry - ly) / H),
            }
        )
    report["elements"]["TITLE_FONT_SIZE"] = layout.title_font.size
    if layout.fits_one_line is not None:
        report["elements"]["TITLE_FIT_TEST"] = {
            "fits_one_line": layout.fits_one_line,
            "max_width_frac": opts.max_title_width_frac,
        }

    if layout.version_rect:
        lx, ly, rx, ry = layout.version_rect
        report["elements"]["VERSION_TEXT_RECT"] = {
            "x": frac(lx / W),
            "y": frac(ly / H),
            "w": frac((rx - lx) / W),
            "h": frac((ry - ly) / H),
        }
        report["elements"]["VERSION_FONT_SIZE"] = layout.version_font.size

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canvas-height", type=int, default=1024)
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
    parser.add_argument("--clearance-w-frac", type=float, default=LayoutOptions.clearance_w_frac)
    parser.add_argument("--clearance-h-frac", type=float, default=LayoutOptions.clearance_h_frac)
    parser.add_argument("--max-title-width-frac", type=float, default=LayoutOptions.max_title_width_frac)
    parser.add_argument("--font-path", default=str(FONT_DEFAULT))
    args = parser.parse_args()

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
        clearance_w_frac=args.clearance_w_frac,
        clearance_h_frac=args.clearance_h_frac,
        max_title_width_frac=args.max_title_width_frac,
        font_path=Path(args.font_path),
    )

    try:
        layout = compute_layout(args.canvas_height, title_lines, args.version, Path(args.logo) if args.logo else None, opts)
    except (FileNotFoundError, ValueError) as exc:
        sys.exit(str(exc))

    json.dump(layout_report(layout, opts), sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
