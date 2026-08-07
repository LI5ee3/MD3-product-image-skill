---
name: md3-product-main-image
description: >-
  Generate e-commerce product main images for marketplaces like Ozon using
  Google Material Design 3 (MD3) with a master-template-first workflow.
  Use when the user asks to create a product main image or master image,
  replace the product in an approved master with another color SKU, or
  batch-generate a main-image set for multiple SKUs of the same product.
---

# MD3 Product Main Image

## Scope

- GPT-image generation only. Do not use Photoshop, PSD, JSX scripts, website
  builders, or pipeline tools.
- One independent MD3 master per product. Different products may use different
  layouts. Only same-product color variants share one locked layout.
- All outputs are 1200 × 1600 px portrait images suitable for Ozon.

## Determine the mode

Read the request and attached images, then select exactly one mode:

| Mode | Use when | Required inputs |
| --- | --- | --- |
| CREATE_MASTER | No approved master exists for this product | brand logo, product PNG, product name, version text, product color |
| REPLACE_VARIANT | An approved master exists and one other color SKU must be generated | approved master image, product PNG, product name, version text, SKU color |
| BUILD_SKU_SET | Multiple color SKUs of one product must be generated as a set | brand logo, base product PNG, full SKU list (PNG + color per SKU), product name, version text |

State rules:

- If the user has confirmed a master (for example, says "master confirmed" or
  "母版确认") or references an approved master, use REPLACE_VARIANT or
  BUILD_SKU_SET. Never return to CREATE_MASTER for that product.
- If no approved master is referenced, default to CREATE_MASTER.
- If the user starts a new product, treat it as a fresh master even if other
  products already have masters.

## Workflow

### CREATE_MASTER

1. Verify inputs: logo, product PNG, product name, version text, product color.
2. Read `prompts/create-master.md` and fill every placeholder.
3. Attach the brand logo and product PNG to the image-generation request.
4. Generate at 1200 × 1600 px.
5. QA the result with `references/design-rules.md`; regenerate if any check fails.
6. Present the result as the candidate master and ask the user to confirm it
   before it becomes the locked master.

### REPLACE_VARIANT

1. Verify inputs: approved master, new product PNG, SKU name, SKU color,
   product name, version text.
2. Read `prompts/replace-variant.md` and fill every placeholder.
3. Attach the locked master and the new product PNG to the image-generation
   request, in that order.
4. Generate at 1200 × 1600 px.
5. QA lock compliance with `references/design-rules.md`; regenerate only within
   allowed changes. Never redesign the composition.

### BUILD_SKU_SET

1. Verify inputs: logo, base product PNG, product name, version text, and the
   complete SKU list with one PNG and color per SKU.
2. Generate the master first using the CREATE_MASTER workflow and
   `prompts/create-master.md`.
3. QA the master, then treat it as locked for this batch.
4. For each remaining SKU, one at a time, generate the variant using the
   REPLACE_VARIANT workflow and `prompts/replace-variant.md` with the same
   locked master.
5. QA each variant before starting the next SKU.
6. Never design variants independently, in parallel, or from scratch.
7. Deliver the set as: master + one 1200 × 1600 image per SKU, each labeled
   with its SKU name or color.

## Lock rules (all modes)

The master fixes these values; variants must preserve them:

- Logo position and size.
- Product name position, size, and Bold 700 weight.
- Version text position, size, and Medium 500 weight.
- Product name-to-version spacing and alignment.
- Product showcase area position and size.
- Background geometry shape types, positions, and sizes.

Variants may change only:

- Product PNG.
- Background main color.
- Background geometry colors.
- Shadow strength.
- Text lightness or darkness, only when needed for contrast.

## QA before delivery

Run every output through the checklist in `references/design-rules.md`:

- Canvas is 1200 × 1600 px.
- Only allowed content appears; no extra text, selling points, promo labels,
  badges, prices, or extra icons.
- Product name is one line, or at most two when necessary; Bold 700.
- Version text sits below the product name; Medium 500.
- Product and background are clearly separated.
- Variants match the locked master layout.

Regenerate if any item fails. If regeneration still fails after two attempts,
report the specific failed checks instead of delivering.

## References

- `prompts/create-master.md` — master generation prompt.
- `prompts/replace-variant.md` — locked variant replacement prompt.
- `prompts/build-sku-set.md` — batch SKU set prompt and workflow.
- `references/design-rules.md` — design, color, typography, and QA rules.

