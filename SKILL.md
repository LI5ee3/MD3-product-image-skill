---
name: md3-product-image
description: Create exact portrait 3:4 Google Classic MD3 e-commerce product images with one coherently generated product scene, a source-faithful logo, strong exact typography, independent master candidates, and locked-layout SKU variants with visibly SKU-adaptive background palettes. Use when creating a product main image, exploring master candidates, or replacing the product with another SKU while preserving an approved master.
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

Before prompting, inspect the Logo's visible artwork and set one `TITLE_MODE`:

- `WORDMARK_BRAND`: only when the Logo clearly spells the same complete brand name at its planned final size, regardless of case or styling, and contains no product-name words
- `FULL_NAME`: for a symbol, abbreviation, unreadable or ambiguous wordmark, any uncertain case, or an explicit requirement to repeat the brand as text

Set `RENDERED_TITLE` to the remaining product name in `WORDMARK_BRAND`, otherwise to the complete product name.
Treat Logo plus title as the complete product identity; never repeat the brand in `WORDMARK_BRAND`. Lock both values after master approval.

For an SKU variant, also require the user-approved `ORIGINAL MASTER` and current SKU product reference.

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

Allowed transitions are `CREATE_MASTER_OPTIONS -> WAIT_FOR_MASTER_SELECTION`,
`WAIT_FOR_MASTER_SELECTION -> CREATE_MASTER_OPTIONS` for another candidate,
`WAIT_FOR_MASTER_SELECTION -> REPLACE_VARIANT` after explicit selection, and
`REPLACE_VARIANT -> REPLACE_VARIANT` with the exact same `ORIGINAL MASTER`.

### CREATE_MASTER_OPTIONS

Generate one standalone candidate and stop. If the user requests another
candidate, begin again from the original product, original Logo, and exact
text. Do not redesign a rejected candidate or automatically inherit its
composition, palette, placement, geometry, lighting, or mood.

### WAIT_FOR_MASTER_SELECTION

Wait for explicit selection. Bind only the exact selected final asset as the
immutable `ORIGINAL MASTER` for the current SKU set. Do not infer selection,
blend rejected candidates, create a substitute master, or derive SKU variants
from an unselected candidate.

Only an explicit request to end this SKU set and start a new master-selection
workflow may release this binding. A request for another SKU never does.

### REPLACE_VARIANT

Use the exact bound `ORIGINAL MASTER` as the composition reference and the
current SKU product reference as the authoritative product source. Generate
the SKU and its environmental response coherently; do not paste it onto the
master. Derive every SKU directly from this `ORIGINAL MASTER` and `CURRENT SKU`,
never from the latest output or another generated SKU.

Every output is a `SKU_VARIANT`, never a candidate or master. Save it separately;
never overwrite, rename, relabel, copy, or bind it as `ORIGINAL MASTER`. After
delivery, remain in `REPLACE_VARIANT` with the same immutable master binding.

Preserve the approved master:

- Logo artwork, visible scale, and position
- title mode, rendered-title and version typography
- information-group geometry
- product display region and visual-scale logic
- background structure and geometry
- overall composition and primary light direction

Lock the background's structure, geometry, color-role relationships, and
relative light-dark hierarchy, but do not lock its actual hues or palette.

When the current SKU's dominant product color differs visibly from the master
SKU, re-derive the background base and supporting colors from the current SKU.
This palette adaptation is mandatory, not optional. At least one large
background field and one supporting field must change visibly at thumbnail
size. Changing only the product color does not satisfy this requirement.

Keep the new palette coordinated with the current SKU while preserving clear
product-background separation. Do not make the background so similar to the
product that its silhouette becomes weak.

Only the current product source, background color assignments, necessary shadow
strength, subtle separation light, and text lightness for contrast may change.
Keep sibling SKU backgrounds distinguishable at thumbnail size without
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

The exact product identity and later information text are:
- Complete product identity: "[FULL PRODUCT NAME]"
- Rendered product title: "[RENDERED TITLE]"
- Title mode: "[WORDMARK_BRAND or FULL_NAME]"
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

Reserve wide continuous negative space in the upper-left area for the later information group
and its first one-line fit test. Size it from the rendered-title length before placing the product.

The area must support the rendered title at a strong, clearly readable scale and extend far enough downward
for the first title line to begin around 16%-20% of canvas height.
Do not pre-commit to two lines or create a narrow area that forces small text.

Do not generate any card, panel, container, backing plane, pill, plaque,
rectangle, border, frame, isolated color field, or local repair area behind the
information group.

Keep the product as the first visual focus. Reserve enough space for the rendered product title
to become the second visual focus, followed by the Logo and version text.

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
avoidance requirement. Append this SKU palette block without weakening it:

```text
Lock the ORIGINAL MASTER's background geometry, shape placement, depth,
materials, relative light-dark hierarchy, composition, and primary light
direction. Do not lock or copy its actual background hues.

Compare the CURRENT SKU's dominant product color with the ORIGINAL MASTER
product. When they differ visibly, re-derive the background base and supporting
colors from the CURRENT SKU. The background palette must visibly change; this
is mandatory, not optional.

Change the color of at least one large background field and one supporting
field so that the master and current SKU backgrounds remain clearly
distinguishable at thumbnail size. A product-only color change does not count
as background palette adaptation.

Preserve the number, geometry, position, depth, material, and visual role of
the master background fields. Change their color assignments without
redesigning the layout. Do not preserve the master hues merely because the
master is used as a reference image.

Derive the new palette from the CURRENT SKU without prescribing specific
colors. Maintain clear contrast between the CURRENT SKU and every adjacent
background field so that the product remains the first visual focus.
```

Before generation, verify that the outbound prompt contains:

- exact portrait `3:4`
- the complete unified-scene requirement
- the no-background-only requirement
- the unchanged Google Classic MD3 style block
- upper-left continuous negative space without a panel
- product/background silhouette separation
- one product only
- no generated information-group Logo or typography
- the selected `TITLE_MODE` and exact `RENDERED_TITLE`
- in `REPLACE_VARIANT`, the exact bound `ORIGINAL MASTER`, not the latest output
- for a visibly different SKU color, the mandatory SKU palette block and a
  thumbnail-visible background change rather than a product-only color change

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
- for an SKU whose dominant product color visibly differs from the master, the
  background palette remains materially the same at thumbnail size
- an SKU changes only the product color without changing at least one large
  background field and one supporting field
- an adapted background becomes too similar to the current SKU and weakens its
  silhouette
- forbidden content appears

If the scene fails, discard it and regenerate the complete scene from the
original inputs. Do not repair, inpaint, extend, locally erase, or use the
failed image as a reference.

## Add one exact information group

After scene acceptance, add the original Logo and exact typography directly to
the continuous upper-left negative space.

Order the group vertically:

1. Logo
2. rendered product title
3. version text, when supplied

Use the Logo's visible artwork left edge as the shared visual left axis. Ignore
the transparent PNG canvas boundary. Keep the complete group in the upper half
and outside the product's core display area.

Treat the Logo and the title-plus-version text block as two coordinated units.
Keep the Logo in its safe position. Prefer the first title line's visible top at
approximately 16%-20% of canvas height, with deliberate breathing room below the
Logo; do not pull the text upward merely to compact the group. Treat this as
visual guidance, not a pixel-perfect threshold. Move title and version together.
For global repositioning move both units together; lock both positions and their spacing after master approval.

## Enforce the visual hierarchy

The mandatory viewing order is:

1. product
2. rendered product title
3. Logo
4. version text

The order must remain obvious at normal and thumbnail size. The rendered title
must attract attention before the Logo. A correctly sized Logo still fails if
it becomes more prominent than the title.

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

Do not crop, crowd an edge, make the Logo unrecognizably small, or measure its transparent canvas.
Size from visible artwork bounds on both axes, never height alone. Apply these rules:

- preferred visible height: 4.5%-6% of canvas height when width stays compliant
- visible width: no more than 30% of canvas width; exceeding this is a hard fail
- left safe margin: approximately 5% of canvas width or more
- top safe margin: approximately 5% of canvas height or more

For an extra-wide wordmark, the width cap and third-level hierarchy override the height recommendation.
Preserve proportions and allow a recognizable height below 4.5%; passing the height range never excuses excessive width or prominence.

During independent master exploration, let Logo scale adapt naturally. After
selection, lock the Logo artwork, visible scale, and position for every SKU.

## Set typography by hierarchy

Render the exact `RENDERED_TITLE` and version text. Preserve all characters,
capitalization, punctuation, spacing, language, and word order. Do not translate,
rewrite, abbreviate, invent, or duplicate text.

Use clean, restrained Google Classic MD3 sans-serif typography with enough
weight for clear recognition. Avoid thin, light, condensed, stretched,
distorted, or disproportionately spaced lettering.

### Break the rendered title correctly

Use no more than two lines. Always fit-test the exact `RENDERED_TITLE` as one line
first at the preferred visible letter height. Measure it in the actual information
area and validate hierarchy before creating separate text objects or a line break.

Keep one line when it fits without shrinking, distortion, crowding, overlap, or loss of the second
visual level. Use two lines only after that test fails; record which condition failed. Separate brand
and remaining-name inputs are content fields, not permission to split by default.

After a failed test:

- `WORDMARK_BRAND`: wrap only the remaining product name at a natural word boundary; never repeat the brand
- `FULL_NAME`: put `[BRAND]` alone on line 1 and `[PRODUCT NAME OR MODEL WITHOUT BRAND]` on line 2

Never split a word, add a third line, reorder text, or make either line resemble
a label or subtitle. Both lines must read as one title group.

### Keep the rendered title strong

Prefer a visible letter height of approximately 4%-5% of canvas height for each title line.
Measure visible letters, not nominal point size or invisible font metrics.

This range is visual guidance, not a pixel-perfect threshold. Regardless of the
measured percentage, fail typography that appears small at normal size, becomes
difficult to read at thumbnail size, or attracts less attention than the Logo.

If the rendered title cannot fit within two lines at the required strength, enlarge the
reserved information area or regenerate the scene with a better composition.
Do not compensate by shrinking the title, adding a third line, splitting words,
distorting letters, compressing spacing excessively, overlapping the product,
or leaving the information group.

### Keep the version subordinate

Place the exact version text below the rendered title. Prefer a visible letter height of
approximately 2%-2.5% of canvas height; keep it legible but subordinate to the title and Logo.

If no version text is supplied, omit the version line without inventing a replacement.

After master approval, lock `TITLE_MODE`, rendered-title and version content,
visible scale, placement, line breaks, spacing, and hierarchy for every SKU.

## Limit visible content

Allow only:

1. the source Logo
2. the exact `RENDERED_TITLE`
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
- the product, rendered title, Logo, and version do not read in the required order
- the rendered title is small, weak, or difficult to read
- the Logo attracts attention before the rendered title or exceeds 30% visible canvas width
- the Logo differs from its source or receives an added color, background,
  gradient, lighting effect, or dimensional treatment
- the information group sits on a card, frame, panel, backing shape, or isolated
  color field
- required text is missing, changed, misspelled, reordered, duplicated, or
  unreadable
- title content does not match `TITLE_MODE`, or `WORDMARK_BRAND` repeats the brand
- a two-line title lacks a recorded failed one-line fit-and-hierarchy test
- a two-line title violates its mode-specific line-break rule
- the information group lacks one left axis, leaves the upper half, intrudes
  into the product area, or pins the title block too close to the Logo or top edge
- the product is changed, cropped, duplicated, poorly integrated, or insufficiently
  separated from the background
- forbidden visible content appears
- a master candidate depends on a rejected candidate
- an SKU changes locked master geometry, composition, or lighting structure
- an SKU with a visibly different product color fails mandatory background
  palette adaptation
- an SKU derives from another generated SKU
- an SKU output is labeled, saved, treated, or rebound as `ORIGINAL MASTER`
- the bound `ORIGINAL MASTER` changes or is overwritten after SKU generation

If only the Logo or typography fails, preserve the accepted unified scene and
rebuild the complete information group from the original Logo and exact text.
Do not locally repair part of a damaged Logo or word.

If the required typography cannot fit, treat it as a scene failure and regenerate from the
original inputs with more continuous space. Never shrink the title to preserve a failed composition.

Deliver only after every applicable check passes.
