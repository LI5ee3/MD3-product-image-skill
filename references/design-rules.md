# Design Rules — v4.0

## Core Principle

Constrain visual outcomes, not specific hues.

## Canvas

- strict 3:4
- target 1200 × 1600 px

## Logo

- uploaded logo is an indivisible protected graphic
- upper-left safe area only
- minimum left clearance: 60 px
- minimum top clearance: 80 px
- maximum bounding box: 220 × 100 px
- preserve original aspect ratio
- never re-typeset embedded wordmark text

## Information Zone

- title and version stay in upper half
- title below logo
- preferred title-left alignment with logo-left edge
- version aligns with title
- maintain breathable logo-to-title spacing
- maintain stable title-to-version spacing
- text block must not invade product core display area
- long titles: maximum two lines

## Product

- uploaded PNG is authoritative
- no redraw
- no recolor
- no structural modification
- proportional scale and placement only
- restrained natural shadows allowed

## MD3

Target:
- bright
- light
- lively
- youthful
- clean
- breathable
- modern
- e-commerce friendly

Use:
- rounded geometry
- curves
- tonal surfaces
- soft gradients
- subtle elevation
- generous whitespace

Avoid:
- Android-app UI look
- oppressive heavy-dark mood
- theatrical black-studio treatment
- bulky pedestal dominance
- excessive visual effects

## Adaptive Color

No fixed background palette.

No product-color-to-background-color lookup table.

Every product and every master candidate independently evaluates:

- luminance
- saturation
- material
- visual weight
- local accents
- silhouette separation
- composition
- MD3 tonal balance
- marketplace thumbnail readability

Use luminance separation to preserve product clarity.
Keep hue adaptive.

### Dark products

Require enough luminance separation.
Do not prescribe hue.

### Light products

Require enough silhouette/luminance separation.
Do not prescribe hue.

### Colored products

Do not mechanically match product hue.
Do not mechanically use a complementary hue.
Let palette selection remain free.
Hard requirements:
- clear product/background separation
- lively modern e-commerce result

## Candidate Diversity

Five candidates:
- separate images
- meaningfully different compositions
- color evaluated independently
- no forced color-family quotas
- no forced hue differences
- similar palettes are allowed when genuinely appropriate

## Variant

Lock:
- logo
- text
- information zone
- product visual-size logic
- product center
- background geometry
- composition

Adapt:
- background color
- geometry fill colors
- tonal-surface colors
- shadow intensity
- subtle separation light
- text light/dark value when needed

Every SKU re-evaluates its palette independently.
Do not inherit the previous SKU palette as a default.
