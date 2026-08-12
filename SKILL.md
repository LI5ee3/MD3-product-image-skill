---
name: md3-product-image
description: "Create portrait 3:4 Google Classic MD3 e-commerce product images with Image Gen backgrounds and exact locally composited transparent products, fixed 2D shadows, Logo, and Roboto Bold text. Use for product main images, master selection, or locked-layout SKU variants."
---

# MD3 Product Image

## Resolve inputs once

Reuse paths and values already known in the current task. Do not access historical
memory, prior sessions, or earlier product outputs. Use only current uploads and
the explicitly bound master in the current product directory.

For the first master request, require:

- authoritative transparent product PNG
- original transparent Logo PNG
- complete product name, brand, remaining name/model, and optional version
- `TITLE_LINES`: `1` (`一行`) or `2` (`两行`)
- `LOGO_TYPE`: `GRAPHIC` (`图形`) or `TEXT` (`文字`)

Never infer `TITLE_LINES` or `LOGO_TYPE`. If either is absent, stop and request:

```text
产品名称显示行数：[一行/两行]
品牌 Logo 类型：[图形/文字]
```

Require `完整产品名称 == 品牌 + 一个空格 + 其余名称`. For `TEXT`, render only
the remaining name; for `GRAPHIC`, render the complete name. Never repeat a
text Logo brand in the title.

## Keep one product in one directory

Use `<output root>/<exact complete product name>` as `PRODUCT_DIRECTORY`.
Never abbreviate or slugify it. Write every workflow artifact for that product
inside this directory.

- Keep `layout.json`, `master.json`, cached Logo/text assets, scenes, prompt and
  attempt records, failure records, candidate files, and thumbnails in
  `PRODUCT_DIRECTORY`.
- Keep only `output/ORIGINAL_MASTER_FINAL.png` and
  sequential `output/SKU_VARIANT-A.png`, `SKU_VARIANT-B.png`, and so on in
  `output`.
- Never put a thumbnail, candidate, scene, manifest, or temporary file in
  `output`.

## Run the fixed workflow

Use:

`MEASURE -> BUILD_PROMPT -> IMAGE_GEN_BACKGROUND -> BACKGROUND_CHECK -> LOCAL_SCENE_COMPOSITE -> COMPOSITE_CHECK -> CANDIDATE -> USER_APPROVAL -> BIND -> SKU`

Image Gen creates only the empty MD3 background. Locally add the exact
transparent product, deterministic 2D shadow, Logo, and text in that order.

### 1. Measure once

Run `scripts/measure_text.py` with the authoritative transparent product PNG as
`--product-reference`, `--logo`, exact names,
`--logo-type`, `--title-lines`, optional `--version`, and `--output-root`.
Always use bundled `assets/Roboto-Bold.ttf`; never substitute a font.

The script creates the product directory, `layout.json`, the alpha-cropped Logo,
and title/version masks. It rejects a product without a usable transparent PNG
alpha channel and records source product and Logo measurements.
Reuse them without remeasurement, recropping, or rerendering for every retry and
SKU. Stop if the selected title line count cannot fit or any glyph is missing.

### 2. Build the background prompt and call Image Gen

Run:

```text
python scripts/scene_prompt.py build --mode MASTER --layout <layout.json> --target <candidate-id>
```

Use stdout unchanged as the Image Gen prompt. Keep
`references/image-gen-prompt.txt` unchanged. The script appends a layout-only
block that merges the measured Logo, every title-line, and optional version safe
rectangles into one outer rectangle, expands it by `5%` of the canvas on every
side, and clips it to the canvas.
If the same product has failure records, the script then appends their
accumulated temporary correction block. It always appends the canonical product
and shadow placement policy last, so that policy overrides any earlier temporary
correction that requested an empty product or shadow area.

For a master, send only the authoritative transparent product PNG as a palette
reference. Image Gen must not reproduce the product. Do not send the Logo or
text assets. Request portrait 3:4 at the highest practical quality; do not
invent unsupported generator parameters.

When calling Image Gen through `functions.exec`, always forward its return value
with `generatedImage(result)`:

```javascript
const result = await tools.image_gen__imagegen({ ... });
generatedImage(result);
```

Never iterate or forward `result.content`; that can discard a successfully
generated raster. Continue only after the call exposes an accessible saved
background raster.

If generation completes without an accessible raster, record a delivery
failure, then rebuild the same target and call Image Gen again with the unchanged
prompt:

```text
python scripts/scene_prompt.py record-delivery-failure --layout <layout.json> --mode <MASTER|SKU> [--target <candidate-id>] --reason <reason>
```

Use `--target` only for `MASTER`; `SKU` reads its automatic name from the active
run.

A `DELIVERY_FAILED` call is recorded in `scene-attempts.json` but does not use
one of the three complete-background attempts. Never record it with
`record-failure`.

The first build opens one active background run and writes its prompt and attempt
state in `PRODUCT_DIRECTORY`. Reuse the same target for retries. A changed target
requires `--new-candidate`, and that flag is allowed only after the user
explicitly requests another independent candidate. A new candidate inherits
the accumulated corrections for the same complete product name only.

Use `--new-candidate` only for the explicit README request `再创建一个独立母版候选`.

For an SKU, build with:

```text
python scripts/scene_prompt.py build --mode SKU --layout <layout.json> --master <master.json>
```

The script assigns the next unused sequential name (`SKU_VARIANT-A`,
`SKU_VARIANT-B`, and so on), verifies the bound master, appends the same final
merged information safe-zone block, then the minimal SKU edit block from
`references/replace-variant-block.md`, followed by the same product's accumulated
temporary corrections when present, and finally the same canonical product and
shadow placement policy. Send exactly two Image Gen references:
`ORIGINAL_MASTER_BACKGROUND.png` as composition reference and the current
transparent SKU PNG only as palette reference. Image Gen must return an empty
background. Never send `ORIGINAL_MASTER_SCENE.png`,
`ORIGINAL_MASTER_FINAL.png`, Logo, text, masks, or another SKU to Image Gen.

### 3. Reject or accept the background

Reject a generated background when any apply:

- it is not native portrait 3:4
- the final merged information safe rectangle contains a card edge, strong
  shadow, texture change, or detailed geometry
- a product, product-shaped element, product shadow, floor, table, display
  stand, generated Logo, or generated text appears
- the background geometry or MD3 presentation contradicts
  `references/image-gen-prompt.txt`
- an SKU changes the master background composition or fails to adapt its colors
  to the current SKU

The final merged information safe rectangle is the only mandatory empty zone.
At the background-only stage, do not reject a simple, low-detail MD3 card merely
because it lies beneath the future local product or shadow, and never invent or
expand a second empty product or shadow zone. Judge an actual product conflict
only from the complete local preview. Do not accept the attempt or create a
candidate yet.

On background failure, do not save or reuse the failed raster. Record every failed
check/correction pair before any next build, then rebuild the same target prompt:

```text
python scripts/scene_prompt.py record-failure --log <scene-failures.json> --mode <MASTER|SKU> [--target <candidate-id>] --failed-check <check> --correction <correction>
```

Use `--target` only for `MASTER`; `SKU` reads its automatic name from the active
run.

The active run stops after three inspectable complete-background attempts. Delivery
failures do not count. Changing the target cannot reset the count. Failure
records accumulate by complete product name and are appended to every later
Image Gen prompt for that product, including new candidates and SKUs. Each new
failure adds to the existing block; different product names never share it.
Never record a correction requiring a product or shadow coordinate region to be
empty or unobstructed. After a complete preview, a background-caused product
conflict must identify the specific dominant high-contrast edge or dense detail
that competes with the product.

### 4. Preview, then create one master candidate

After the scene-only check passes, run:

```text
python scripts/artifact_flow.py preview --generated-background <background> --product <authoritative-transparent-product.png> --product-dir <PRODUCT_DIRECTORY> --candidate-id <id> [--text-color <RRGGBB>] [--version-color <RRGGBB>]
```

This verifies the master product hash, removes low-alpha legacy shadow from the
transparent PNG, fixes the product at the local placement, and generates one
2D shadow at `50°`. It then composes the cached information group, validates
3:4, and writes the background, placed product layer, shadow mask, scene,
preview, thumbnail, and manifest in `PRODUCT_DIRECTORY`. It leaves
the scene attempt `PENDING` and leaves `output` unchanged. If colors are omitted,
the script chooses readable colors automatically. Before compositing, it also
requires at least `1.5:1` contrast between the visible Logo outer edge and the
scene background beneath it.

Use the visible product bounds to select local geometry. Keep visible height at
`54%` and right margin at `12%`. For aspect ratio `>= 1.35`, use maximum width
`68%` and bottom margin `18%`. For aspect ratio `< 0.90`, use maximum width
`52%` and bottom margin `12%`. Otherwise use maximum width `52%` and bottom
margin `18%`. Use shadow angle `50°`, offset `16%` of the product height, blur
radius `0.7%` of the canvas height, and opacity `28%`.

If preview fails with `LOGO_BACKGROUND_CONTRAST_TOO_LOW`, no preview is kept.
Record it as a background failure and regenerate the background; do not run
`discard-preview`, recolor the Logo, or add a backing.

Inspect the full preview and thumbnail. Reject it if the product is cropped or
altered, the fixed 2D shadow does not visibly follow its silhouette at `50°`,
or Logo, text, product, shadow, or a dominant background boundary visibly
conflicts. A simple card beneath the product or cast shadow is not itself a
conflict. For a background-caused failure, run:

```text
python scripts/artifact_flow.py discard-preview --product-dir <PRODUCT_DIRECTORY> --candidate-id <id>
python scripts/scene_prompt.py record-failure --log <scene-failures.json> --mode MASTER --target <id> --failed-check <check> --correction <correction>
```

Never edit `scene-attempts.json`, delete a candidate manifest manually, or reuse
a failed preview. Rebuild the same target background after recording the
failure. If the transparent product itself fails, stop and request a corrected
PNG instead of regenerating the background.

If the preview passes, run:

```text
python scripts/artifact_flow.py candidate --product-dir <PRODUCT_DIRECTORY> --candidate-id <id>
```

This verifies and promotes the exact inspected preview without recompositing,
then marks the attempt `ACCEPTED` and removes the preview artifacts. Show the
candidate and canonical product-directory path, then stop. Never copy it into a
sibling `outputs` directory, infer approval, or bind automatically.

### 5. Bind only explicit user selection

After explicit approval, run:

```text
python scripts/artifact_flow.py bind --product-dir <PRODUCT_DIRECTORY> --candidate-id <id>
```

This verifies candidate hashes, creates immutable-by-workflow
`ORIGINAL_MASTER_BACKGROUND.png`, `ORIGINAL_MASTER_PRODUCT.png`,
`ORIGINAL_MASTER_SHADOW.png`, `ORIGINAL_MASTER_SCENE.png`,
`output/ORIGINAL_MASTER_FINAL.png`, and `master.json`, and consolidates the
selected candidate files. `master.json`
binds the one `layout.json` by hash and locks title/version colors. Binding also
closes the accepted master run by clearing `active_run_id`, so the first SKU can
start a new run normally. Never create or copy a second layout file, edit bound
files, overwrite a master, or relabel an SKU as master.

### 6. Create an SKU final

After the SKU background passes visual review, run:

```text
python scripts/artifact_flow.py sku --generated-background <background> --product <current-transparent-SKU.png> --product-dir <PRODUCT_DIRECTORY>
```

Never ask for or infer an SKU label from user text or upload paths. The script
reads the automatically assigned name from the active SKU run, verifies the
master before and after, reuses the bound layout and fixed 2D shadow parameters,
locally composes the current transparent product and cached Logo/text, and
writes only the final SKU to `output`; its background, product layer, shadow
mask, scene, and thumbnail stay in `PRODUCT_DIRECTORY`. It adapts both title and version
colors to the current SKU scene background. Version text must have lower visual
contrast than the title while remaining readable against its background. Never
overwrite an existing SKU. If Logo/background contrast is below `1.5:1`, record
the SKU background failure and regenerate the SKU background.

## Preserve the information group

Add only the exact source Logo, title, and optional version in that vertical
order on one uninterrupted background. The mandatory attention order is:
product, title, Logo, version.

- Preserve Logo artwork, alpha, color, letterforms, spacing, proportions, and
  edges. Allow only proportional scaling and positioning; use visible alpha
  bounds, not transparent canvas bounds. Never redraw, retype, recolor, deform,
  relight, texture, or add a backing/effect. Require at least `1.5:1` contrast
  between its visible outer edge and the background beneath it.
- Preserve every text character, case, punctuation mark, space, language, and
  word order. Use only Roboto Bold and the manually selected line count.
- For two lines with `GRAPHIC`, use brand on line 1 and remaining name on line
  2. For two lines with `TEXT`, split only the remaining name at a natural word
  boundary and never repeat the brand.
- Keep the Logo and text on the visible Logo left edge. Keep clear line gaps at
  full size and `288 x 384`. Keep the gap from the last title line to the version
  text at `2.5%` of the canvas height for both one-line and two-line titles.
- Render version text in its measured size. Its solid color must have lower
  visual contrast than the title while remaining clearly readable. Do not force
  an absolute brightness gap that makes the version more prominent. Never use
  outline, glow, shadow, or backing.

If only local information rendering fails, reuse the accepted background,
placed product, shadow, and cached assets; never remeasure. If a protected zone
or background boundary fails, regenerate only the background. Do not inpaint,
erase, extend, or repair a failed background.

Deliver only after deterministic script checks and the visual checks above pass.
