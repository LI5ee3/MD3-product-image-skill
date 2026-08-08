# MD3 Product Main Image Skill v4.0

v4.0 is a clean rebuild of the workflow rather than another patch on top of v3.x.

The major change is the color system.

## v4.0 Color Philosophy

Previous versions became too prescriptive by listing preferred background colors for certain product colors.

That can create a new bias: the model may repeatedly choose the same “safe” palette even when the product changes.

v4.0 removes those fixed color lists.

The new principle is:

**Constrain the visual result, not the specific hue.**

The Skill now controls:

- product/background separation;
- thumbnail readability;
- visual lightness;
- MD3 mood;
- commercial clarity.

It does NOT prescribe a specific hue family.

## Dark Products

For low-luminance products:

- maintain enough luminance separation;
- usually avoid making most of the canvas equally dark;
- do not prescribe a specific background hue.

## Light Products

For high-luminance products:

- maintain enough silhouette and luminance separation;
- do not prescribe a specific background hue.

## Colored Products

For visibly colored products:

- do not mechanically match the product hue;
- do not mechanically apply a complementary hue;
- let palette choice remain free.

There is intentionally no “can use…” color list.

## Candidate Color Logic

The five master candidates do not need to use five different color families.

Composition is the primary source of candidate diversity.

Each candidate independently evaluates its best palette.

Do not:

- copy the previous candidate palette mechanically;
- force a hue difference merely for novelty;
- impose color-family quotas.

## Variant Color Logic

Every SKU re-evaluates its palette independently.

The master locks:

- composition;
- logo;
- information zone;
- product visual-size logic;
- product center;
- background geometry.

The SKU may adapt:

- background main color;
- MD3 geometry fill colors;
- tonal-surface colors;
- shadow intensity;
- separation light;
- text light/dark value when necessary.

The target is:

**same master structure, independently optimized MD3 palette for each SKU.**

---

# Standard Workflow

## 1. New Product

Upload:

- brand logo
- product PNG

Provide:

- product name
- version text

Generate five standalone master candidates.

If the interface cannot reliably generate five separate images at once, generate one candidate at a time.

## 2. Select Master

Explicitly select one original candidate.

That original image becomes ORIGINAL MASTER.

## 3. Generate Variants

For each additional SKU:

Image A = ORIGINAL MASTER  
Image B = current SKU PNG

Never use a previously generated SKU variant as Image A.

## 4. Batch SKU

Choose the master SKU first.

Generate and select its master before generating any remaining SKU.

---

# Layout Rules

- strict 3:4
- target 1200 × 1600 px
- logo upper-left safe area
- minimum left clearance 60 px
- minimum top clearance 80 px
- logo max 220 × 100 px
- product name and version remain in the upper half
- product name below logo
- product name preferably left-aligned with logo
- version left-aligned with product name
- stable vertical spacing
- long title maximum two lines

---

# Recommended Usage Prompt

## Start a new product

Use the text in:

`prompts/create-master.md`

## Lock a master

Use:

`prompts/select-master.md`

## Replace a SKU

Use:

`prompts/replace-variant.md`

## Batch multiple SKUs

Use:

`prompts/build-sku-set.md`

---

# File Structure

- `SKILL.md`
- `README.md`
- `prompts/create-master.md`
- `prompts/select-master.md`
- `prompts/replace-variant.md`
- `prompts/build-sku-set.md`
- `references/design-rules.md`
