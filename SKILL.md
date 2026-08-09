---
name: md3-product-image
description: Create portrait 3:4 Google Classic MD3 e-commerce product images with one coherent scene, visibly shallow 2.5D background geometry and platform, an exact source Logo, strong exact typography with unbacked version text, independent master candidates, and locked-layout SKU variants with SKU-adaptive palettes. Use for product main images, master exploration, master selection, or another SKU derived from an approved ORIGINAL MASTER.
---

# MD3 Product Image

## Load once and resolve inputs

Read this file once per task turn. Do not reread it unless the file changes.
Reuse already resolved inputs from the current context; do not reopen a complete
prior task or image payload merely to rediscover known paths or text.

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

Use these exact local font files for every task:

- `TITLE_FONT_PATH=/System/Library/Fonts/Supplemental/Arial Bold.ttf`
- `VERSION_FONT_PATH=/System/Library/Fonts/Supplemental/Arial Bold.ttf`

Call these paths directly. Do not search for, select, or silently substitute
another font. Stop and report if either file is unavailable or any required
character cannot be rendered.

Before the first generation call:

1. Confirm generation can receive every scene reference, exact portrait 3:4,
   and the highest practical quality. Keep the Logo out of scene generation.
2. Confirm the exact source Logo and typography can be added afterward. Stop if
   required inputs, exact 3:4, or exact composition is unavailable.
3. Use GPT Image 2 only when explicit model selection confirms it; otherwise
   use the available generator without claiming a model.
4. Load `TITLE_FONT_PATH` and `VERSION_FONT_PATH` with the renderer that will
   compose the final image.
5. With that same renderer and those exact files, measure actual visible glyph
   bounds at the target title and version scales. Fit-test the title as one line
   first.
6. At the planned Logo scale, measure its visible artwork. Calculate concrete
   normalized `x/y/w/h` rectangles for `INFORMATION_GROUP_RECT`, `LOGO_RECT`,
   `TITLE_RECT`, and `VERSION_TEXT_RECT`; use `INFORMATION_GROUP_RECT` as the
   single `INFORMATION_CLEAR_ZONE` sent to scene generation. Keep the title's
   first visible line around 16%-20% of canvas height with deliberate space
   below the Logo.
7. Size `VERSION_TEXT_RECT` from the measured version glyphs plus comfortable
   clearance, reserving the required title-to-version gap before it; set it to
   `NONE` when absent. Verify all internal rectangles fit inside the clear zone
   without touching product or internal boundaries.
8. Resolve every bracketed prompt field to concrete values before generation.
   Keep exact future Logo, title, and version content out of the scene prompt;
   stop rather than send any unresolved template token.

Do not invent parameters the generator does not expose or require a fixed pixel
resolution.

## Pass the style unchanged

Append this block to every scene prompt without changing any word:

```text
Use Google Classic Material Design 3 (MD3) as the sole visual style.

Do not use Material 3 Expressive.
```

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

Treat any earlier master containing an information backing as incompatible.
Never remove or ignore its locked geometry for an SKU; start a new master workflow.

After approval, lock Logo, title mode, exact text, typography, line breaks,
information-group geometry, product display logic, background structure/material
roles, composition, relative light-dark hierarchy, and primary light direction.

## Build the canonical scene prompt

Include this `CORE_SCENE_BLOCK` in every call. Replace only brackets, adapt the
declared input role, and append the unchanged style block.

```text
Create one portrait 3:4 e-commerce product image using the supplied inputs.

Input role: [MASTER: Image 1 is authoritative product / SKU: ORIGINAL MASTER is
composition reference and CURRENT SKU is authoritative product]. The original
Logo PNG is excluded. Do not render or approximate information-group Logo or text.

Future information is excluded from this call. Protect only this normalized
canvas area; never infer or render its future content:
- invisible information clear zone: [INFORMATION_CLEAR_ZONE as x/y/w/h]

The clear zone is uninterrupted base-field negative space, not a rectangle or
scene object. Do not show its bounds or place any panel, bar, card, plaque,
backing, edge, shadow, platform, or separate surface inside it.

Generate the complete product scene now. Product, environment, platform,
lighting, shadows, reflections, ambient response, perspective, scale, and
spatial relationships must form one coherent image. Do not generate a
background-only image or leave product placement for later compositing.

Create a graphic-first Google Classic MD3 product showcase with large overlapping 2.5D rounded panels, 2.5D organic geometric fields, restrained physical depth, matte surfaces, soft elevation, and a low 2.5D product platform. Keep it spacious and layered, not a realistic room, architectural interior, furniture scene, or physical exhibition environment.

Make every major background rounded panel and organic geometric field visibly
shallow 2.5D scene geometry, never a flat filled region. Show visible shallow
edge thickness plus overlap, occlusion, or a short soft elevation shadow that
follows the primary light direction. Keep the depth restrained and graphic;
do not turn these fields into walls, architecture, or a deep 3D set.

Derive the palette from the current product without prescribing colors.
Preserve authentic product colors. Adjust platform and adjacent-field hue and
lightness so the entire silhouette, lower body, and contact area remain clear
at normal and thumbnail size. When hues are similar, create a clear light-dark
difference. Do not rely on saturation, partial contrast, outlines, halos,
glows, or product backing. The platform top must not merge with the product.

Render exactly one faithful product. Preserve identity, geometry, proportions,
construction, materials, controls, display content, colors, and details. Do not
redesign, deform, simplify, recolor, replace, duplicate, or invent components.
Match lighting, perspective, reflections, contact shadows, and ambient occlusion;
reject floating or pasted-on appearance.

Keep the declared information clear zone as wide continuous upper-left negative
space. Do not let the product, a background boundary, or any visible information
backing enter it. Treat canvas, product, and internal shape boundaries as
usable-area edges. Touching, crossing, or tangent contact fails.

Keep product first in focus, future title second, Logo third, and version fourth.
Use clean high-key studio lighting from a large upper-front soft source, gentle
fill, restrained separation light, short diffused contact shadows, and
controlled reflections.

Outside authentic product markings, generate no text, Logo, letters, numbers,
icons, labels, badges, prices, specifications, slogans, promotions, or
watermarks. Avoid information cards, extra backing shapes, multiple products,
duplicate-like reflections, rooms, furniture, shelves, props, boxes, detailed
scenery, busy patterns, neon, glassmorphism, excessive gradients, deep
perspective, product deformation, extra text, and marketplace graphics.
```

For `REPLACE_VARIANT`, append:

```text
Lock ORIGINAL MASTER geometry, shape placement, depth, material roles,
relative light-dark hierarchy, composition, and primary light direction. Use
CURRENT SKU as the only authoritative product; do not show the master product.

Do not lock master hues. When CURRENT SKU visibly differs in dominant color,
re-derive the background base and secondary colors from CURRENT SKU. At least
one large field and one secondary field must change visibly at thumbnail size;
a product-only change does not count. Preserve separation from every adjacent field.

Lock version-text size, position, and typography. Its solid lightness may adapt
only for legibility against the SKU-adaptive background; never add a backing.
```

Before generation, confirm 3:4, unified scene, one faithful product, separation,
visibly shallow 2.5D major fields, one resolved invisible information clear zone,
no future Logo/text content or backing, and the unchanged style block. For an
SKU, also confirm the exact bound master and palette rule.

## Retry without prompt expansion

If the scene fails, discard it and regenerate from original inputs. Reuse the
same `CORE_SCENE_BLOCK`, style block, bracket values, and applicable SKU block
unchanged. Append only:

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
- the information clear zone is interrupted, reveals a visible boundary or
  backing, or cannot fit the planned information group with required clearance
- an SKU violates the bound master, direct derivation, palette adaptation, or
  product separation
- forbidden content appears

## Add the exact information group

After scene acceptance, add only original Logo and exact typography in this
vertical order: Logo, rendered title, version directly on the uninterrupted
background. Use the Logo artwork's visible left edge as the shared text axis;
ignore transparent PNG bounds. Compose within the planned internal rectangles,
in the upper half and outside the product region and all boundaries. Never move
the title upward, shrink it, or shift one element alone to rescue a failed scene;
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

Use at most two lines; never split a word or turn a line into a subtitle. If it
cannot fit strongly, regenerate more space rather than shrink or distort it.

Place exact version text directly on the uninterrupted background inside
`VERSION_TEXT_RECT`, using the same typography measured in preflight. Prefer
visible height 2.75%-3.25% of canvas height and about 55%-65% of title height,
bold weight, and a clearly separated title-to-version gap of about 1.0-1.4
version-letter heights. Use one solid text color with sufficient contrast.
Hierarchy must come from lower emphasis, not miniature type. Never abbreviate,
outline, glow, shadow, or add a panel, bar, card, plaque, or backing.

Mandatory order: product, title, Logo, version. After approval, lock all content,
scale, position, spacing, and line breaks; only permitted SKU version-text
lightness adaptation may change.

## Validate and deliver

Validate the final 3:4 file at full size and an Ozon-like `288 x 384` thumbnail
shown at 100% without zoom. Reject when exact hierarchy, source Logo, exact text,
marketplace readability, planned rectangles, title mode, line breaking, shared
axis, boundary clearance, direct version-text contrast, absence of information
backings, product fidelity/separation, allowed content, master binding, or SKU
adaptation fails.

If only Logo or typography fails, preserve the accepted scene and rebuild the
complete information group from original assets. If information clear-zone
geometry, placement, or clearance fails, regenerate the complete scene. Never
repair an individual glyph or Logo fragment. Deliver only after every applicable
check passes.
