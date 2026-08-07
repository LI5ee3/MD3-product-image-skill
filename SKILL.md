---
name: md3-product-main-image
description: >
  Create Google Material Design 3 inspired e-commerce product main images
  with GPT-image. Supports creating one independent master image for a product,
  replacing same-product color SKU variants while locking the approved master,
  and generating complete multi-color SKU sets using a master-first workflow.
---

# MD3 Product Main Image

## Purpose

Create premium 1200 × 1600 px e-commerce product main images for marketplaces
such as Ozon using GPT-image.

Each product gets its own independently designed master image.

Different products do NOT need to share the same layout.

The only global requirement across products is the Google Material Design 3
visual direction and the generation rules defined in this Skill.

For the SAME product with different colors:

- Create one master first.
- Lock the master.
- Generate all remaining color SKUs by editing/replacing the product inside
  that master.

Never independently redesign every color SKU.

---

# Supported Modes

The Skill supports exactly three workflow modes:

1. CREATE_MASTER
2. REPLACE_VARIANT
3. BUILD_SKU_SET

Determine the correct mode before generating images.

---

# MODE 1 — CREATE_MASTER

Use when:

- the product does not yet have an approved master;
- the user asks to create a product main image or master;
- the user specifies one color as the master;
- the user uploads a logo and product PNG for a new product.

Read:

`prompts/create-master.md`

Generate ONE master image.

Do not automatically generate other SKU colors unless the user explicitly
requests batch generation.

---

# MODE 2 — REPLACE_VARIANT

Use when:

- an approved master already exists;
- the user supplies another color PNG of the same product;
- the user asks to replace the product color;
- the user says the master is confirmed, approved, locked, finalized, or
  equivalent.

Read:

`prompts/replace-variant.md`

CRITICAL:

Once the user confirms a master, NEVER return to CREATE_MASTER for other
colors of that same product unless the user explicitly asks to redesign the
master.

Treat the task as editing the master, NOT creating a new poster.

---

# MODE 3 — BUILD_SKU_SET

Use when:

- the user uploads several colors of the same product;
- the user asks to generate all color variants;
- the user asks for a complete SKU image set.

Read:

`prompts/build-sku-set.md`

The workflow MUST be:

MASTER SKU
→ CREATE MASTER
→ lock master
→ Variant 2 replacement
→ Variant 3 replacement
→ Variant N replacement

Never independently generate multiple posters in parallel.

There must be ONE layout origin for the entire set.

---

# Required Inputs

## CREATE_MASTER

Required:

- uploaded brand logo;
- uploaded product PNG;
- product name;
- version text.

If multiple product colors are already uploaded, identify which color should
serve as master.

If the user explicitly chooses one, use it.

If no master color is specified but multiple colors exist, prefer the variant
with the clearest silhouette and strongest neutral visual balance.

Do not ask unnecessary questions when the correct choice is obvious.

---

## REPLACE_VARIANT

Required:

- approved master image;
- new same-product color PNG.

Do not regenerate a replacement if there is no usable master image available.

---

## BUILD_SKU_SET

Required:

- brand logo;
- product name;
- version text;
- at least two same-product color PNGs.

Optional:

- user-selected master color.

---

# Product Identity

Use uploaded product PNGs as the authoritative reference.

Preserve:

- silhouette;
- proportions;
- case;
- strap;
- buttons;
- crown;
- product materials;
- product viewing angle;
- screen appearance;
- distinctive physical details.

Do not redesign the physical product.

Do not convert it into a different model.

---

# Allowed Visible Content

Outside text that naturally exists inside the product render/screen, the
generated main image may contain ONLY:

- uploaded brand logo;
- product name;
- version text;
- uploaded product;
- MD3-inspired background geometry;
- lighting and shadows.

Do NOT add:

- feature descriptions;
- specification text;
- selling points;
- promotional copy;
- discount labels;
- certification labels;
- additional logos;
- extra symbols;
- badges;
- decorative English words;
- invented UI;
- invented marketplace stickers.

---

# Canvas

Target:

1200 × 1600 px

Aspect ratio:

3:4

Composition must remain suitable for Ozon-style marketplace thumbnails.

Keep critical content away from extreme edges.

---

# Typography

## Product Name

Use:

- modern neutral sans-serif;
- Material / Roboto / Google Sans inspired appearance;
- Bold;
- approximately weight 700.

The product name must be highly visible.

Prefer one line.

If the product name is too long:

1. retain one line if readable;
2. moderately reduce font size;
3. if still necessary, use maximum two lines.

Do not excessively shrink long product names.

Do not split words internally.

Use semantic line breaks.

Example:

Xiaomi Smart Band 11
Active

is valid.

---

## Version

Use:

- Medium;
- approximately weight 500.

Version text must remain prominent and readable.

It should be visually secondary to the product name but should NOT look like
fine print.

Do not use:

- extremely small text;
- low opacity;
- Light 300;
- very pale text merely to create hierarchy.

Hierarchy should primarily come from:

Product name = Bold 700

Version = Medium 500

---

# Information Layout

The brand logo, product name, and version form one information hierarchy.

The exact layout may vary between different products.

Do not force all products into one universal template.

The layout should respond to:

- product silhouette;
- product-name length;
- viewing angle;
- product color;
- visual weight.

Background decoration must adapt around the information area.

Text must not be sacrificed to preserve decoration.

---

# Logo

Use the uploaded logo faithfully.

Do not redraw, reinterpret, replace, distort, recolor, or invent the logo.

The logo should remain visible but should not dominate the product.

For same-product SKU variants, logo size and placement must remain visually
unchanged.

---

# MD3 Design Direction

Use Google Material Design 3 principles as visual inspiration.

Preferred elements:

- rounded geometry;
- tonal surfaces;
- soft gradients;
- large abstract curves;
- rounded panels;
- restrained depth;
- subtle elevation;
- clean visual hierarchy;
- generous spacing;
- adaptive color.

Do NOT turn the image into an Android app interface.

This is an e-commerce product visual inspired by MD3, not an application UI.

---

# Background Geometry

Background geometry should support the product rather than compete with it.

It may include:

- large arcs;
- partial circles;
- rounded tonal fields;
- simple curved surfaces;
- subtle gradients.

Strong geometric edges must avoid:

- brand logo;
- product name;
- version text.

Maintain visual clearance around important text.

If geometry conflicts with information:

1. move geometry;
2. scale geometry;
3. simplify geometry.

Never reduce readability to preserve decoration.

---

# Product Priority

The product is the main visual subject.

It should:

- occupy substantial image area;
- remain clearly recognizable at marketplace thumbnail size;
- have clear silhouette separation;
- receive appropriate lighting;
- retain realistic product proportions.

Avoid making the product unnecessarily small because of decorative elements.

---

# Lighting

Use premium restrained studio lighting.

Allowed:

- controlled key light;
- subtle highlights;
- realistic contact shadow;
- soft ambient shadow;
- gentle separation light where required.

Avoid:

- excessive bloom;
- cinematic smoke;
- dramatic lens flares;
- exaggerated neon;
- unrealistic reflections.

---

# Color System

Different SKU colors may use different MD3 theme colors.

They do NOT need identical background colors.

However, the same-product layout remains locked.

## Dark Products

Suitable themes:

- graphite;
- charcoal;
- dark cool gray;
- dark neutral surfaces.

Ensure dark straps/cases remain visible against the background.

---

## Light / Colored Products

Suitable themes:

- cool gray;
- warm gray;
- muted complementary tones;
- low-saturation tonal surfaces.

Do not match the background too closely to the product color.

---

## White Products

Do not place white products on nearly pure-white backgrounds.

Prefer:

- greige;
- taupe;
- stone;
- beige-gray;
- warm neutral;
- muted cool gray.

Maintain clear edge separation.

---

# MASTER LOCK

Once a master image is approved, lock its visual structure.

For all same-product variants preserve:

- logo visual size;
- logo location;
- product-name size;
- product-name location;
- version size;
- version location;
- title/version spacing;
- text alignment;
- product display area;
- product visual size;
- product visual center;
- background geometry shape;
- background geometry size;
- background geometry position;
- general lighting direction;
- overall composition.

Allowed SKU-specific changes:

- product PNG;
- background main color;
- background geometry color;
- shadow strength;
- text light/dark value only where required for contrast.

Do NOT modify:

- composition;
- layout;
- typography geometry;
- background geometry structure;
- product placement logic.

---

# CREATE_MASTER Procedure

When mode = CREATE_MASTER:

1. Inspect uploaded logo.
2. Inspect product PNG.
3. Analyze product silhouette and dominant color.
4. Analyze product-name length.
5. Design one independent MD3 composition suitable for this product.
6. Select background color that separates product from background.
7. Generate exactly one master image.
8. Verify output using Final QA.

The master should be good enough to serve as the only visual reference for
later SKU replacements.

---

# REPLACE_VARIANT Procedure

When mode = REPLACE_VARIANT:

1. Treat Image A as the locked approved master.
2. Treat Image B as the replacement product PNG.
3. Do NOT create a new composition.
4. Replace the product.
5. Match the original product visual size.
6. Match the original product center.
7. Match the original placement logic.
8. Keep logo and typography visually unchanged.
9. Keep background geometry structurally unchanged.
10. Adapt theme colors only when required by the new product color.
11. Verify using Variant QA.

The desired result should look like the same design file with a different
product color inserted.

---

# BUILD_SKU_SET Procedure

When mode = BUILD_SKU_SET:

1. Inspect all uploaded same-product PNGs.
2. Identify the master SKU.
3. Generate ONE master using CREATE_MASTER rules.
4. Treat that result as the locked layout reference.
5. For each remaining color:
   - use the locked master as Image A;
   - use the new color PNG as Image B;
   - apply REPLACE_VARIANT rules.
6. Never independently generate variants without referencing the master.
7. Run SKU Set QA after all variants are complete.

Conceptually:

SKU 1
→ CREATE_MASTER
→ MASTER

MASTER + SKU 2 PNG
→ REPLACE_VARIANT

MASTER + SKU 3 PNG
→ REPLACE_VARIANT

MASTER + SKU N PNG
→ REPLACE_VARIANT

Do not use:

SKU 1 → independent generation
SKU 2 → independent generation
SKU 3 → independent generation

---

# Final QA — Master

Before accepting a master verify:

- exact product name;
- exact version text;
- correct uploaded logo;
- no unwanted text;
- no invented selling points;
- no extra badges;
- no extra labels;
- product is clearly dominant;
- product/background contrast is sufficient;
- typography is readable;
- version is clearly visible;
- background geometry does not interfere with text;
- overall visual direction is recognizably MD3-inspired;
- image works as an e-commerce main image.

If major problems exist, regenerate the master.

---

# Variant QA

For every variant compare against the approved master.

Check:

- logo has not visibly moved;
- logo has not visibly resized;
- product name has not visibly moved;
- product name has not visibly resized;
- version has not visibly moved;
- version has not visibly resized;
- text spacing remains consistent;
- product visual scale remains consistent;
- product center remains consistent;
- background geometry has not changed structure;
- background geometry has not visibly moved;
- only appropriate theme colors changed;
- no additional text appeared.

If a variant looks like a newly redesigned poster, reject it and regenerate as
a locked-master replacement.

---

# SKU Set QA

When generating multiple color SKUs:

Rapidly compare all images mentally as a sequence.

They should feel like:

same template
+
different product color
+
different coordinated MD3 color theme

They should NOT feel like separate posters.

If an element visibly jumps between images, regenerate the affected variant
using the approved master as the stronger reference.

---

# User Approval State

If the user says:

- approved;
- confirmed;
- this is the master;
- lock this version;
- use this for the other colors;
- this one is good;

mark the current image conceptually as MASTER_APPROVED.

From that point onward:

same-product colors MUST use REPLACE_VARIANT or BUILD_SKU_SET continuation.

Do not silently redesign the master.
