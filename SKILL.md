---
name: md3-product-image
description: "Create portrait 3:4 Google Classic MD3 e-commerce product images: one coherent scene with shallow 2.5D geometry, an exact source Logo, exact typography, independent master candidates, and locked-layout SKU variants with SKU-adaptive palettes. Use for product main images, master exploration, master selection, or SKUs derived from an approved ORIGINAL MASTER."
---

# MD3 Product Image

## Load once and resolve inputs

Read this file once per task turn. Do not reread it unless the file changes.
Reuse already resolved inputs from the current context; do not reopen a complete
prior task or image payload merely to rediscover known paths or text.

Never read from historical memory, prior sessions, or earlier outputs of any
kind. Derive everything only from current uploads and the explicitly bound
`ORIGINAL MASTER` of this session; do not recall, reconstruct, or reuse any
prior candidate, SKU, palette, text, or composition from memory.

For a master candidate, require product reference as Image 1, original Logo PNG
as Image 2, exact complete product name, brand, remaining name/model after the
brand, and optional exact version text. Confirm that brand plus remaining name
reproduces the complete name. Never render placeholders.

Inspect the Logo at planned size and set one `TITLE_MODE`:

- `WORDMARK_BRAND`: only when the Logo clearly spells the complete brand,
  contains no product-name words, and remains readable at final size
- `FULL_NAME`: for a symbol, abbreviation, ambiguous or unreadable wordmark,
  any uncertainty, or an explicit request to repeat the brand

Set `RENDERED_TITLE` to the remaining name in `WORDMARK_BRAND`; otherwise use
the complete name. Logo plus title must reproduce the identity without brand
duplication. For an SKU, also require the explicitly approved `ORIGINAL MASTER`
and current SKU product reference.

## Run preflight and measure text

Use these exact font files bundled with this skill for every task:

- `TITLE_FONT_PATH=assets/Roboto-Bold.ttf`
- `VERSION_FONT_PATH=assets/Roboto-Bold.ttf`

Call these paths directly relative to the skill folder; never substitute
another font. Stop and report if a file is unavailable or a character cannot
render.

Before the first generation call:

1. Confirm generation can receive every scene reference, exact portrait 3:4,
   and the highest practical quality. Keep the Logo out of scene generation.
2. Confirm the exact source Logo and typography can be added afterward. Stop if
   required inputs, exact 3:4, or exact composition is unavailable.
3. Call the Image Gen tool to output the image.
4. Run `scripts/measure_text.py` with the resolved title, optional version, and
   Logo to measure exact visible glyph and artwork bounds using
   `TITLE_FONT_PATH` and `VERSION_FONT_PATH`.
5. Use its `TITLE_FIT_TEST` for the one-line fit test. Keep the title's first
   visible line around 16%-20% of canvas height with deliberate space below the
   Logo.
6. From the script output, collect the concrete normalized `x/y/w/h` rectangles
   for `LOGO_RECT` and each `TITLE_LINE_RECT`.
7. From the script output, size `VERSION_TEXT_RECT` with the measured version
   glyphs and the title-to-version gap; set it to `NONE` when absent.
8. Use the script's connected stepped zones as `INFORMATION_CLEAR_ZONES`; never
   replace them with the outer bounding rectangle. Treat padding as optical
   guidance, not a pixel-perfect threshold.
9. Verify the zones fit the canvas and avoid the product region; validate
   background boundaries after scene generation.
10. Resolve every bracketed prompt field to concrete values before generation.
   Keep exact future Logo, title, and version content out of the scene prompt;
   stop rather than send any unresolved template token.

Do not invent parameters the generator does not expose or require a fixed pixel
resolution.

## Build the canonical scene prompt

Read `references/core-scene-block.md`. Append its `CORE_SCENE_BLOCK` unchanged
to every scene call, replacing only brackets and adapting the declared input
role; append its style block unchanged. For an SKU (`REPLACE_VARIANT`), also
read `references/replace-variant-block.md` and append its block unchanged.
Never rewrite, paraphrase, or expand them.

Before generation, confirm 3:4, unified scene, one faithful product, separation,
visibly shallow 2.5D major fields, controlled hue-family contrast with matched
perceived saturation, one resolved connected stepped information clear area, no
future Logo/text content or backing, and the unchanged style block. For an SKU,
also confirm the exact bound master and palette rule.

## Use the fixed workflow and state

Use:

`PREFLIGHT -> MEASURE_TEXT -> BUILD_PROMPT -> GENERATE_SCENE -> VALIDATE_SCENE -> ADD_INFORMATION_GROUP -> VALIDATE_FINAL -> DELIVER`

Generate product, environment, platform, lighting, shadows, reflections,
ambient response, perspective, scale, and spatial relationships together.
Never create a background-only image and later paste in the product. Only the
original Logo and exact typography may be added after scene acceptance. Never
generate or add a backing for Logo, title, or version text.

Use one state:

- `CREATE_MASTER_OPTIONS`: generate one independent candidate and stop. Another
  candidate restarts from original inputs and inherits nothing rejected.
- `WAIT_FOR_MASTER_SELECTION`: bind only an explicitly selected final asset as
  immutable `ORIGINAL MASTER`; never infer selection.
- `REPLACE_VARIANT`: derive every SKU directly from that same master plus
  `CURRENT SKU`, never from another SKU or the latest output.

Save every SKU separately as `SKU_VARIANT`; never overwrite, relabel, copy, or
bind it as master. Only an explicit request to end the SKU set and start a new
master workflow releases the binding.

A master containing an information backing is incompatible; start a new master
workflow, never reuse its geometry for an SKU.

After approval, lock Logo, title mode, exact text, typography, line breaks,
information-group geometry, product display logic, background structure/material
roles, composition, relative light-dark hierarchy, and primary light direction.

## Retry without prompt expansion

If the scene fails, discard it and regenerate from original inputs. Reuse the
same `references/core-scene-block.md` and `references/replace-variant-block.md`
blocks and bracket values unchanged. Append only:

```text
RETRY_CORRECTION:
- [observed failed check] -> [one concrete required correction]
```

Record validation failures before retrying. Every recorded failure must appear
once in the correction block; omit satisfied rules and generic restatements.
Do not rewrite, paraphrase, or expand the base prompt. Make at most three
complete-scene attempts; after the third failure, stop and report them. Never
repair, inpaint, extend, locally erase, or use a failed scene as reference.

## Validate the scene

Reject when any apply:

- canvas is not exact portrait 3:4 or is cropped from another ratio
- product fidelity, single-product count, integration, lighting, perspective,
  contact shadow, or adjacent-field separation fails
- product is not the first focus
- any major background panel or organic geometric field reads only as a flat
  fill or gradient, lacks visible shallow depth, or breaks the light direction
- major panels and fields collapse into one repeated near-identical hue family,
  or the contrast family is excessively saturated, widely repeated, or becomes
  a focal point that breaks the mandatory visual hierarchy
- a protected information content zone or connector is interrupted, reveals a
  visible boundary or backing, or cannot fit the planned information with
  required clearance
- an SKU violates the bound master, direct derivation, palette adaptation, or
  product separation
- forbidden content appears

A boundary outside every protected zone is not a failure merely because it lies
inside their overall outer bounds. Reject only when it enters protected geometry
or visibly fragments the information group at full or thumbnail size. Minor
deviation in optional outer padding is not a hard failure when optical clearance
and readability remain sound.

## Add the exact information group

After scene acceptance, add only original Logo and exact typography in this
vertical order: Logo, rendered title, version directly on the uninterrupted
background. Run `scripts/compose_image.py` on the accepted scene with the
resolved title, optional version, and Logo; it renders the exact typography
from `TITLE_FONT_PATH`/`VERSION_FONT_PATH` and pastes the Logo at the planned
content rectangles, so the composite matches the measured clear zones exactly.
Use the Logo artwork's visible left edge as the shared text axis;
ignore transparent PNG bounds. Compose within the planned content rectangles,
in the upper half, inside the stepped clear area, and outside the product region.
Never move the title upward, shrink it, or shift one element alone to rescue a failed scene;
regenerate the scene instead. Move title and version together; move Logo and the
text unit together globally.

### Preserve the Logo

Use Image 2 as one exact flat asset. Allow only proportional scaling and
positioning. Preserve artwork, color, transparency, letterforms, spacing,
proportions, and edges. Never redraw, retype, split, rearrange, recolor, deform,
simplify, relight, texture, reflect, replace, or add a backing/effect.

Measure visible artwork, not transparent canvas:

- preferred height: 4.5%-6% of canvas height when width remains valid
- maximum visible width: 30% of canvas width; exceeding it is a hard fail
- preferred left and top margins: about 5% of canvas width and height

Never crop, crowd, or make it unrecognizable. Width cap and third-level hierarchy
override height guidance. Any Logo that attracts attention before title fails.

### Set exact typography

Preserve every character, case, punctuation mark, space, language, and word
order. Render the title only with `TITLE_FONT_PATH` and the version only with
`VERSION_FONT_PATH`. Never synthesize weight, condense, stretch, distort, or
substitute either font.

Prefer title visible letter height around 4%-5% of canvas height. Keep the
measured one-line title when it fits strongly. Only after a recorded failed test:

- `WORDMARK_BRAND`: wrap remaining name at a natural boundary; never repeat brand
- `FULL_NAME`: brand alone on line 1, remaining name/model on line 2

For a two-line title, measure the actual visible glyph bounds. Keep a clear gap
between line 1's visible bottom and line 2's visible top, preferably about
0.4-0.55 of one title line's visible letter height. Treat this as optical
guidance, not fixed pixels. Reject touching, tangent, or compressed lines, or
lines that lose clear separation in the `288 x 384` thumbnail.

Use at most two lines; never split a word or turn a line into a subtitle. If it
cannot fit strongly, regenerate more space rather than shrink or distort it.

Place exact version text directly on the uninterrupted background inside
`VERSION_TEXT_RECT`, using the same typography measured in preflight. Prefer
visible height 2.75%-3.25% of canvas height and about 55%-65% of title height,
bold weight. Measure the title-to-version gap from the final title line's visible
bottom to the version text's visible top. Use about 1.0-1.4 version-letter
heights for a one-line title and a tighter 0.75-1.0 for a two-line title. Reject
crowding or a version line that appears detached from the title block at full
size or in the `288 x 384` thumbnail. Use one solid text color with sufficient
contrast. Hierarchy must come from lower emphasis, not miniature type. Never abbreviate, outline, glow, shadow, or add any backing.

Mandatory order: product, title, Logo, version. After approval, lock content,
scale, position, spacing, and line breaks per the lock list; only SKU
version-text lightness may adapt.

## Validate and deliver

Run `scripts/validate_final.py` on the final file; it rejects any canvas that is
not an exact portrait 3:4 and writes the `288 x 384` thumbnail. Then validate
the full-size file and that thumbnail shown at 100% without zoom. Reject when
exact hierarchy, source Logo, exact text,
marketplace readability, planned content rectangles and stepped clear zones,
title mode, line breaking and spacing, title-to-version gap, shared axis,
boundary clearance, direct
version-text contrast, absence of information backings, product
fidelity/separation, allowed content, master binding, or SKU adaptation fails.

If only Logo or typography fails, preserve the accepted scene and rebuild the
complete information group from original assets. If protected content-zone or
connector geometry, placement, or clearance fails, regenerate the complete
scene. Never repair an individual glyph or Logo fragment. Deliver only after every applicable
check passes.
