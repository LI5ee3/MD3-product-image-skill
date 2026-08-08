---
name: md3-product-image
description: Create exact portrait 3:4 Google Classic MD3 e-commerce product images with one coherently generated product scene, a source-faithful logo, strong exact typography, independent master candidates, and locked same-product SKU variants. Use when creating a product main image, exploring master candidates, or replacing the product with another SKU while preserving an approved master.
---

# MD3 Product Image

## Require the source inputs

For a master candidate, require:

- Image 1: product reference
- Image 2: original Logo PNG
- exact complete product name
- exact brand text
- exact remaining product-name or model text after the brand
- exact version text, when required

Confirm that the brand followed by the remaining product-name text preserves the
complete product name exactly. Never render placeholder labels or brackets.

For an SKU variant, also require the user-approved `ORIGINAL MASTER` and the
current SKU product reference.

## Run generation preflight

Before building a prompt:

1. Confirm that an image-generation tool is available.
2. Confirm that it can receive the product reference and every scene reference
   required for the current state. Keep the Logo out of scene-generation calls.
3. Use GPT Image 2 only when explicit model selection is available and confirms
   that model. Otherwise use the available capability without naming or
   assuming its model.
4. Request the highest practical image quality.
5. Request an exact portrait 3:4 aspect ratio when the interface exposes that
   control. Do not invent unsupported model, quality, or size parameters.
6. Confirm that the original Logo and exact text can be added afterward without
   redrawing, recoloring, or altering them.
7. Stop and report the missing capability if exact 3:4 generation, required
   scene inputs, or exact information-group composition cannot be supported.

Do not require a fixed pixel resolution.

## Pass the visual style unchanged

Pass the Google Classic MD3 style instruction to the image generator unchanged:

```text
Use Google Classic Material Design 3 (MD3) as the sole visual style.

Do not use Material 3 Expressive.
```

Do not reword, summarize, expand, or replace this style block.

## Follow the execution sequence

Use this sequence for every final output:

`PREFLIGHT -> BUILD_PROMPT -> GENERATE_SCENE -> VALIDATE_SCENE -> ADD_INFORMATION_GROUP -> VALIDATE_FINAL -> DELIVER`

The product, environment, platform, lighting, shadows, reflections, ambient
color, perspective, scale, and spatial relationships must be generated
together as one coherent scene.

Never generate a background-only image for later product placement. Never
paste, alpha-composite, or programmatically overlay the product onto a completed
background.

Only the original Logo PNG and exact specified typography may be added after an
accepted unified product scene has been generated.

Make at most three complete-scene attempts for one output. If the third attempt
still fails scene validation, stop and report the failed items. Never deliver a
failed result as valid.

## Use one workflow state at a time

Use exactly one of these states:

1. `CREATE_MASTER_OPTIONS`
2. `WAIT_FOR_MASTER_SELECTION`
3. `REPLACE_VARIANT`

### CREATE_MASTER_OPTIONS

Generate one standalone candidate and stop. If the user requests another
candidate, begin again from the original product, original Logo, and exact
text. Do not redesign a rejected candidate or automatically inherit its
composition, palette, placement, geometry, lighting, or mood.

Natural similarity is acceptable only when it follows from an independent
design decision.

### WAIT_FOR_MASTER_SELECTION

Wait for explicit selection. Only the selected final image becomes the
`ORIGINAL MASTER`.

Do not blend rejected candidates, create a substitute master, or derive SKU
variants from an unselected candidate.

### REPLACE_VARIANT

Use the `ORIGINAL MASTER` as the composition reference and the current SKU
product reference as the authoritative product source. Treat this as locked
master replacement, not a new poster design.

Generate the current SKU and its environmental response coherently. Do not
paste the SKU onto the master. Derive every SKU directly from the
`ORIGINAL MASTER` and `CURRENT SKU`; never derive one generated SKU from
another.

Preserve the approved master:

- Logo artwork, visible scale, and position
- product-name and version typography
- information-group geometry
- product display region and visual-scale logic
- background structure and geometry
- overall composition and primary light direction

Only the current product source, coordinated background colors, necessary
shadow strength, subtle separation light, and text lightness for contrast may
change. Keep sibling SKU palettes distinguishable at thumbnail size without
changing the locked layout.

## Build the mandatory scene prompt

Include the following block in every master scene-generation prompt. Replace
only bracketed values and append the unchanged Google Classic MD3 style block.
Do not summarize, omit, or weaken its requirements.

```text
Create one portrait 3:4 e-commerce product image using the supplied inputs.

Image 1 is the product reference and must be used as the primary image input.
The original Logo PNG is intentionally excluded from this scene-generation
call. Do not render or approximate the information-group Logo; the exact source
Logo will be added after the unified scene passes validation.

The later exact information text is:
- Complete product name: "[FULL PRODUCT NAME]"
- Brand: "[BRAND]"
- Remaining product name or model: "[PRODUCT NAME OR MODEL WITHOUT BRAND]"
- Version text: "[VERSION TEXT]"

Generate the complete unified product scene now. The first generated image must
already contain the product in its final environment and approximate final
composition.

Generate the product, environment, platform, lighting, shadows, reflections,
ambient color, perspective, scale, and spatial relationships together as one
coherent image.

Do not generate or save a background-only image. Do not leave product placement
for later compositing.

Create a graphic-first Google Classic MD3 product showcase using large
overlapping rounded panels, soft 2.5D organic geometric fields, restrained
physical depth, matte surfaces, soft elevation, and a low product platform.

Keep the composition spacious, balanced, clean, and visually layered without
becoming a realistic room, architectural interior, furniture scene, or physical
exhibition environment.

Derive the tonal palette from the current product. Do not prescribe specific
colors. Use one neutral base and a small number of coordinated, low-saturation
supporting tones.

Place a contrasting tonal field behind the product so that its complete
silhouette remains clearly separated from the environment. Do not allow a
white, dark, or similarly colored product to blend into nearby background
shapes.

Render the product from Image 1 as the primary physical subject. Preserve its
identity, geometry, proportions, construction, materials, controls, display
content, colors, and fine details.

Do not redesign, deform, simplify, recolor, replace, duplicate, or invent any
product component.

Environmental lighting may naturally affect product highlights, reflections,
shading, ambient color response, and contact shadows so that it belongs in the
environment. Match light direction, softness, color temperature, perspective,
sharpness, reflections, and depth.

Generate physically coherent contact shadows and ambient occlusion at actual
contact points. Reject cutout edges, halos, generic blurred silhouette shadows,
unsupported floating, missing contact shadows, mismatched illumination, or a
pasted-on appearance.

Use exactly one product. Do not generate additional products, SKU variants,
floating copies, reflections resembling duplicate products, or incomplete
product fragments.

Reserve comfortable continuous negative space in the upper-left area for the
later information group. Determine its required size from the actual complete
product-name length before finalizing product placement.

The reserved area must support the complete product name at a strong, clearly
readable scale. Do not create a narrow information area that would force the
title to become small.

Do not generate any card, panel, container, backing plane, pill, plaque,
rectangle, border, frame, isolated color field, or local repair area behind the
information group.

Keep the product as the first visual focus. Reserve enough space for the
complete product name to become the second visual focus, followed by the Logo
and version text.

Use clean high-key studio lighting from a large upper-front soft source, gentle
fill light, restrained separation light, soft natural contact shadows, and
subtle controlled reflections. Keep highlights clean and shadows short and
diffused.

Do not generate information-group text, Logo, brand mark, letters, icons,
labels, badges, prices, specifications, slogans, promotional copy, or
watermarks. Preserve only authentic markings already present on the product.

Avoid Material 3 Expressive, background-only generation, later product cutout
compositing, information cards, backing planes, multiple products, duplicate
products, realistic rooms, furniture, shelves, decorative props, product boxes,
detailed scenery, architectural interiors, complex textures, busy patterns,
neon, glassmorphism, excessive gradients, deep perspective, product
deformation, extra text, additional logos, icons, labels, badges, prices,
specifications, slogans, promotional content, and watermarks.
```

For `REPLACE_VARIANT`, adapt only the input roles: use the approved master as
the composition reference and the current SKU image as the authoritative
product. Keep every applicable scene, integration, hierarchy, lighting, and
avoidance requirement.

Before generation, verify that the outbound prompt contains:

- exact portrait `3:4`
- the complete unified-scene requirement
- the no-background-only requirement
- the unchanged Google Classic MD3 style block
- upper-left continuous negative space without a panel
- product/background silhouette separation
- one product only
- no generated information-group Logo or typography

Correct any omission before calling the image generator.

## Validate the unified scene first

Before adding the Logo or typography, reject the scene if:

- the canvas is not exact portrait 3:4 or was cropped from another ratio
- the product appears pasted onto a separately generated background
- product geometry, controls, display, materials, colors, or identity changed
- lighting, reflections, perspective, contact shadows, or ambient color do not
  match the environment
- the product is not the clear first visual focus
- the product blends into the background
- more than one product or a duplicate-like reflection appears
- the upper-left continuous information area is too small for strong typography
- the information area contains a card, panel, frame, backing shape, or isolated
  color field
- forbidden content appears

If the scene fails, discard it and regenerate the complete scene from the
original inputs. Do not repair, inpaint, extend, locally erase, or use the
failed image as a reference.

## Add one exact information group

After scene acceptance, add the original Logo and exact typography directly to
the continuous upper-left negative space.

Order the group vertically:

1. Logo
2. complete product name
3. version text, when supplied

Use the Logo's visible artwork left edge as the shared visual left axis. Ignore
the transparent PNG canvas boundary. Keep the complete group in the upper half
and outside the product's core display area.

Move the three elements as one group. Do not resize or reposition only the Logo
while leaving the text behind.

## Enforce the visual hierarchy

The mandatory viewing order is:

1. product
2. complete product name
3. Logo
4. version text

The order must remain obvious at normal and thumbnail size. The complete
product name must attract attention before the Logo. A Logo within its suggested
size range still fails if it becomes more prominent than the product name.

## Protect the Logo

Use Image 2 as one exact, flat asset. Treat transparent pixels as transparency,
never as a color or background.

Allow only proportional scaling and positioning. Preserve the original visible
artwork, colors, transparency, letterforms, spacing, proportions, and edge
details.

Do not redraw, retype, split, rearrange, recolor, deform, simplify, relight,
shade, texture, reflect, replace, or add effects. Do not add a backing tile,
gradient, three-dimensional treatment, scene color contamination, or local
repair seam. Environmental lighting must not affect the Logo. Preserve an
effect only when it is intrinsic to the supplied source.

Do not crop, crowd an edge, make the Logo unrecognizably small, or use its
transparent canvas as the measurement boundary.

Use these visual recommendations:

- visible Logo height: 4.5%-6% of canvas height
- left safe margin: approximately 5% of canvas width or more
- top safe margin: approximately 5% of canvas height or more

These are not pixel-perfect failure thresholds. Minor deviation alone is not a
failure when the Logo remains recognizable and correctly occupies the third
visual level.

During independent master exploration, let Logo scale adapt naturally. After
selection, lock the Logo artwork, visible scale, and position for every SKU.

## Set typography by hierarchy

Render the supplied complete product name and version text exactly. Preserve
all characters, capitalization, punctuation, spacing, language, and word order.
Do not translate, rewrite, abbreviate, invent, or duplicate text.

Use clean, restrained Google Classic MD3 sans-serif typography with enough
weight for clear recognition. Avoid thin, light, condensed, stretched,
distorted, or disproportionately spaced lettering.

### Break the product name correctly

Use no more than two lines.

Use one line only when the complete name remains large, strong, readable, and
unmistakably the second visual focus. Never choose a small size merely to keep
the name on one line.

When two lines are required, use exactly:

```text
[BRAND]
[PRODUCT NAME OR MODEL WITHOUT BRAND]
```

Keep the brand alone on line 1 and all remaining product-name or model text on
line 2. Never split a word, add a third line, reorder text, or make the brand
line resemble a small label or subtitle. Both lines must read as one complete
product-name group.

### Keep the product name strong

Prefer a visible letter height of approximately 4%-5% of canvas height for each
product-name line. Measure visible letters, not nominal point size or invisible
font metrics.

This range is visual guidance, not a pixel-perfect threshold. Regardless of the
measured percentage, fail typography that appears small at normal size, becomes
difficult to read at thumbnail size, or attracts less attention than the Logo.

If the name cannot fit within two lines at the required strength, enlarge the
reserved information area or regenerate the scene with a better composition.
Do not compensate by shrinking the title, adding a third line, splitting words,
distorting letters, compressing spacing excessively, overlapping the product,
or leaving the information group.

### Keep the version subordinate

Place the exact version text below the product name. Prefer a visible letter
height of approximately 2%-2.5% of canvas height. Keep it clearly legible but
subordinate to the product name and Logo.

If no version text is supplied, omit the version line without inventing a
replacement.

After master approval, lock the complete product name, version content, visible
scale, placement, line breaks, spacing, and hierarchy for every SKU.

## Limit visible content

Allow only:

1. the source Logo
2. the exact complete product name
3. the exact version text, when supplied
4. the single source product
5. visual elements belonging to the Google Classic MD3 composition
6. restrained supporting lighting and shadows

Authentic text already present on the product may remain. Add no selling points,
specifications, promotions, labels, discounts, certifications, extra Logos,
icons, badges, marketplace stickers, invented UI, or watermarks.

## Validate the final image

Validate only the final exported 3:4 file at normal and thumbnail size.

Reject it if:

- the final canvas is not exact portrait 3:4
- the product, product name, Logo, and version do not read in the required order
- the product name is small, weak, or difficult to read
- the Logo attracts attention before the product name
- the Logo differs from its source or receives an added color, background,
  gradient, lighting effect, or dimensional treatment
- the information group sits on a card, frame, panel, backing shape, or isolated
  color field
- required text is missing, changed, misspelled, reordered, duplicated, or
  unreadable
- a one-line title was made weak merely to avoid the required two-line structure
- a two-line title does not place the brand first and the remaining name second
- the information group lacks one left axis, leaves the upper half, or intrudes
  into the product's core display area
- the product is changed, cropped, duplicated, poorly integrated, or insufficiently
  separated from the background
- forbidden visible content appears
- a master candidate depends on a rejected candidate
- an SKU fails to preserve the approved master or derives from another SKU

If only the Logo or typography fails, preserve the accepted unified scene and
rebuild the complete information group from the original Logo and exact text.
Do not locally repair part of a damaged Logo or word.

If the required typography cannot fit because the information area is too
small, treat it as a scene failure and regenerate the unified scene from the
original inputs with more continuous space. Never shrink the title to preserve
a failed composition.

Deliver only after every applicable check passes.
