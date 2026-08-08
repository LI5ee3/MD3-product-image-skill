---
name: md3-product-image
description: Create 3:4 e-commerce product main images in Google Classic Material Design 3, protect supplied logo and product assets, develop independent master candidates one at a time, and derive same-product SKU variants directly from one user-approved ORIGINAL MASTER. Use when generating a product master image, replacing a product with another SKU, or building a consistent same-product SKU image set.
---

# MD3 Product Image

## Pass the visual style unchanged

Pass the Classic MD3 style instruction to the image generator unchanged:

```text
Use Google Classic Material Design 3 (MD3) as the sole visual style.

Do not use Material 3 Expressive.

Do not interpret Classic MD3 as a realistic room, studio set,
architectural environment, or physical exhibition stage.
```

Do not expand it into prescribed colors, shapes, surfaces, elevation,
lighting, materials, platforms, or scene descriptions.

Add task facts and non-style constraints outside the block. Do not paraphrase
or supplement the block with a fixed MD3 template or prose that translates
Classic MD3 into visual attributes. Let the image generator independently
determine composition, palette, geometry, spatial relationships, lighting, and
visual mood for the current product.

## Follow the execution loop

Use this loop for every output:

`PREFLIGHT -> GENERATE -> VALIDATE`

During `PREFLIGHT`, inspect the outbound generation prompt. If the Classic MD3
style block was changed, paraphrased, or expanded, correct the prompt before
calling the image generator.

Generate the complete image in one pass from the original inputs. Do not repair
a failed hard constraint by locally repainting, inpainting, or regenerating part
of the image. Invalidate the result and regenerate the whole image from its
original inputs.

Make at most three complete-image attempts for one output. If the third attempt
still fails, stop and report the failed validation items. Do not deliver it as
valid.

## Keep the canvas fixed

- Generate exactly one standalone image in each round.
- Deliver a portrait 3:4 image at exactly 1200 x 1600 px.
- Do not create a collage, grid, contact sheet, candidate label, or multi-panel.
- Do not generate at another ratio and crop to 3:4.
- If the generator cannot output 1200 x 1600 directly, accept only an exact 3:4
  source, resize it proportionally without cropping, and verify the final size.
- Do not generate if exact 3:4 cannot be guaranteed.

## Follow the workflow

Use exactly one state at a time:

1. `CREATE_MASTER_OPTIONS`
2. `WAIT_FOR_MASTER_SELECTION`
3. `REPLACE_VARIANT`

### CREATE_MASTER_OPTIONS

Require the source brand logo, source product PNG, exact product name, and exact
version text.

Generate one standalone candidate, then stop. When the user asks for another
candidate, start again from the original logo, original product PNG, product
name, and version text. Do not redesign the previous candidate or automatically
inherit its composition, palette, product placement, logo scale, geometry,
lighting, or visual mood. Natural similarity is acceptable when it is an
independent design decision.

### WAIT_FOR_MASTER_SELECTION

Wait for explicit user selection. Only the selected candidate becomes the
`ORIGINAL MASTER`.

Do not blend rejected candidates, regenerate a substitute master, or derive SKU
variants from an unselected candidate.

### REPLACE_VARIANT

Require:

- Image A: the user-approved `ORIGINAL MASTER`
- Image B: the source PNG for the current SKU

Treat this as locked-master product replacement, not a new poster design.
Derive every SKU directly from `ORIGINAL MASTER + CURRENT SKU`. Never use a
generated SKU variant as the source for another variant.

### Build an SKU set

Treat this as a workflow across the three states, not as a fourth state:

1. Choose the master SKU and enter `CREATE_MASTER_OPTIONS`.
2. Enter `WAIT_FOR_MASTER_SELECTION` after each candidate.
3. After approval, enter `REPLACE_VARIANT` for each remaining SKU.
4. Generate and validate each SKU separately before starting the next.

Do not generate remaining SKUs before master approval or generate multiple SKU
images in one generation.

## Protect the brand logo

Treat the uploaded logo as one indivisible protected graphic. Everything inside
the asset belongs to it, including its symbol, emblem, wordmark, embedded text,
letterforms, spacing, weight, proportions, alignment, colors, transparency, and
edge detail.

Allow only proportional scaling and positioning. Do not recreate, re-typeset,
split, rebuild, recolor, distort, substitute, or reinterpret the logo. Do not
turn embedded logo text into editable typography.

Preserve the transparent-area semantics of the logo source. Place the logo
directly on the image background. Do not add a backing plate or produce a
visible rectangular or square patch around it.

Use the visible artwork bounds, not the transparent PNG canvas bounds, when
judging placement and alignment.

Enforce this visual hierarchy among the three main elements:

1. product: first
2. product name: second
3. logo: third

The logo must never become the first visual focus. This is a hard failure
regardless of its pixel dimensions.

Keep the logo in a comfortable upper-left safe area. For a 1200 x 1600 canvas,
use these approximate visual references:

- left safe margin: about 60 px or more
- top safe margin: about 80 px or more
- preferred visible height: 72-96 px

Use these hard maximums for the logo's visible artwork bounds:

- visible height: 120 px
- visible width: 200 px

The safe margins and preferred height are visual guidelines, not pixel-perfect
validation targets. The maximum height and width are mandatory.

Keep the logo clearly recognizable at normal viewing size. It must not feel
disproportionately small, outrank the product name, touch or visibly crowd an
edge, or be cropped.

Keep the logo flat and source-faithful. Do not let scene lighting affect it,
add a gradient, or apply any three-dimensional treatment. Preserve any such
property only when it is already intrinsic to the supplied logo source.

During master exploration, let logo scale adapt naturally to each independent
composition. After the user selects the `ORIGINAL MASTER`, lock the logo's
artwork, visual size, and position for all SKU variants.

## Build one information group

Treat the logo, product name, and version text as one coherent information
group, not as three unrelated objects.

- Place the product name below the logo and the version below the product name.
- Establish a clear visual left axis using the logo's visible artwork edge.
- Judge alignment optically; do not require mathematical coordinate equality.
- Keep spacing deliberate and visually balanced.
- Keep the group in the upper half and out of the core product display area.
- Preserve the group's complete geometry after `ORIGINAL MASTER` approval.

Do not resize or reposition the logo after generation while leaving the text
behind. If the group is visibly broken, regenerate the complete image from the
original inputs.

## Set typography by hierarchy

Render the supplied product name and version text exactly as provided. Preserve
all characters, capitalization, numbers, punctuation, language, and word order.
Do not translate, rewrite, abbreviate, invent, or duplicate text.

Use a clean, modern, neutral sans-serif treatment compatible with Classic MD3.
Choose font and weight by the intended visual hierarchy.

- Make the product name the clear primary text level.
- Make the version readable but visibly secondary.
- Prefer one line for the product name; use at most two lines when needed.
- Do not split words internally.
- Reduce size moderately when necessary without making the text weak or tiny.
- Keep letterforms clean, undistorted, and legible at normal and thumbnail size.

Treat hierarchy, spacing, line breaking, and optical alignment as visual design
judgments rather than pixel-perfect targets. Incorrect, missing, invented,
duplicated, or unreadable text is a hard failure; a minor stylistic deviation
that preserves the intended hierarchy is not.

After `ORIGINAL MASTER` approval, lock the product-name and version content,
visual scale, placement, line breaks, spacing, and hierarchy for every SKU.

## Protect the product asset

Treat the uploaded product PNG as authoritative. Do not redraw it, substitute a
similar model, recolor it, alter its silhouette, structure, material, screen
proportions, controls, ports, holes, or other real details, add nonexistent
hardware, or remove genuine details.

Allow only proportional scaling, positioning, composition placement, natural
contact shadow, restrained ambient shadow, and subtle separation light when
needed.

## Limit visible content

Allow only:

1. the source brand logo
2. the exact product name
3. the exact version text
4. the source product PNG
5. visual elements belonging to the Classic MD3 composition
6. restrained lighting and shadows supporting the composition

Real text already present on the product may remain.

Do not add selling points, specifications, promotional labels, discounts,
certifications, extra logos, extra icons, badges, decorative copy, marketplace
stickers, or invented UI.

## Lock the approved master

For every SKU variant, preserve the `ORIGINAL MASTER`:

- logo artwork, visual size, and position
- product-name and version typography and information-group geometry
- product display region, visual-scale logic, and visual center
- background structure and geometry
- overall composition and primary light direction

Only these may change for the current SKU:

- source product PNG
- background main color and background-element colors
- shadow strength and subtle separation light when needed
- text lightness when needed for contrast

Do not change anything else from the approved master.

Give sibling color SKUs clearly distinguishable background palettes at
thumbnail size. Do not create distinction by changing the locked layout or by
using arbitrary clashing colors.

## Validate before delivery

Treat these as hard failures:

- output count is not exactly one
- final canvas is not exactly 1200 x 1600 portrait 3:4 or was cropped from another ratio
- logo or product is recreated, altered, distorted, substituted, or cropped
- product, product name, and logo do not read as first, second, and third in
  the visual hierarchy
- logo becomes the first visual focus, regardless of its pixel dimensions
- logo visible artwork exceeds 120 px in height or 200 px in width
- logo is visibly unsafe or unrecognizably small
- scene lighting, an added gradient, or a three-dimensional treatment affects
  the logo
- a visible patch, backing rectangle, or local-repair seam appears around the logo
- required text is incorrect, missing, invented, duplicated, or unreadable
- forbidden text, icon, logo, badge, label, or UI appears
- the result reads as a realistic room, studio set, architectural environment,
  or physical exhibition stage
- the information group lacks a clear visual left axis, leaves the upper half,
  or intrudes into the core product display area
- the product is not clearly recognizable, prominent, and separated from the background
- a master candidate depends on a previous rejected candidate
- an SKU variant fails to preserve the approved master structure
- an SKU variant derives from another generated variant
- sibling SKU palettes are not clearly distinguishable at thumbnail size

Treat approximate logo margins, the preferred 72-96 px logo height, optical
alignment, spacing, font choice, font weight, and line breaking as visual
judgments. The visual hierarchy and 120 px height and 200 px width maximums are
not approximate. Do not fail solely because another guideline differs by a few
pixels while preserving the intended visual result.

If a hard failure occurs, invalidate the entire result and regenerate from the
original inputs, subject to the three-attempt limit. For a master candidate,
use the original logo, product PNG, product name, and version text. For a
variant, use the approved `ORIGINAL MASTER` and current SKU PNG. Never deliver a
locally patched result as valid.
