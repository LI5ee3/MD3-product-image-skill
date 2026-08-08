---
name: md3-product-main-image
version: 4.0
description: >
  GPT-image-only workflow for creating lively, modern MD3 e-commerce product main images.
  Uses adaptive color logic based on the current product and composition, generates master
  candidates as separate images, protects uploaded logos and product assets, and locks the
  selected ORIGINAL MASTER for same-product SKU replacement.
---

# MD3 Product Main Image Skill v4.0

## Purpose

Create premium e-commerce product main images using GPT-image only.

The workflow is optimized for marketplace card browsing such as Ozon:

- strong product recognition at thumbnail size;
- clear title hierarchy;
- lively, modern MD3 visual language;
- protected uploaded logo and product assets;
- stable same-product SKU consistency;
- adaptive color selection without fixed color templates.

The guiding color principle is:

**Constrain the visual result, not the specific hue.**

---

# Workflow States

1. CREATE_MASTER_OPTIONS
2. WAIT_FOR_MASTER_SELECTION
3. REPLACE_VARIANT
4. BUILD_SKU_SET

---

# STATE 1 — CREATE_MASTER_OPTIONS

Use when there is no approved master for the current product.

Create five master candidates for the same product.

## Separate Output Rule

Five candidates means five separate image outputs.

Never create:

- contact sheets;
- collages;
- grids;
- mood boards;
- comparison boards;
- multi-panel layouts;
- five designs inside one canvas.

Each candidate is one complete standalone 3:4 main image.

Do not place candidate numbers inside the artwork.

If the interface cannot reliably output five separate images in one response:

- generate Option 1 only;
- stop;
- wait for the user to request the next option.

Never solve output limitations by combining candidates into one image.

## Candidate Diversity

The five candidates must differ meaningfully in composition.

Candidate diversity should primarily come from:

- product placement;
- product visual scale;
- negative-space distribution;
- product-to-information-zone relationship;
- MD3 geometry;
- curves and arcs;
- tonal-surface structure;
- depth;
- lighting balance;
- overall visual rhythm.

Do not create five near-identical compositions with only small positional or color changes.

Color diversity is not a quota.

Each candidate should independently evaluate the most suitable palette for its own composition.

Do not mechanically copy the previous candidate's palette.

Do not force a different hue merely to make candidates look different.

Similar color families are acceptable if they are genuinely the best fit.

After all five standalone candidates exist:

STOP and wait for explicit user selection.

---

# STATE 2 — WAIT_FOR_MASTER_SELECTION

Lock a master only after an explicit selection such as:

- “方案3”
- “第三张作为母版”
- “选第3个”
- “方案3，就用这个”

Then set:

- MASTER_SELECTED = selected original candidate
- MASTER_APPROVED = true

The selected ORIGINAL image becomes the sole production master.

Do not blend rejected candidates.

If the user asks for another batch of five candidates, return to CREATE_MASTER_OPTIONS.

---

# STATE 3 — REPLACE_VARIANT

Use when:

- Image A = ORIGINAL MASTER
- Image B = new same-product SKU PNG

This is a locked-master replacement, not a poster redesign.

Every variant must be generated directly from:

ORIGINAL MASTER + CURRENT SKU

Never use a previously generated variant as the source for the next variant.

Correct:

- ORIGINAL MASTER + SKU 2
- ORIGINAL MASTER + SKU 3
- ORIGINAL MASTER + SKU 4

Incorrect:

- MASTER → SKU 2 → SKU 3 → SKU 4

---

# STATE 4 — BUILD_SKU_SET

Use when multiple same-product color SKU PNGs are provided.

Workflow:

1. identify the master SKU;
2. generate five standalone master candidates for that SKU;
3. stop;
4. wait for explicit master selection;
5. lock the selected ORIGINAL MASTER;
6. generate all remaining SKUs directly from that ORIGINAL MASTER.

Never generate remaining SKUs before the master is selected.

---

# Canvas Rule

Every generated image must use:

- strict aspect ratio: 3:4
- target size: 1200 × 1600 px

Applies to:

- master candidates;
- selected master;
- variant replacements;
- batch SKU outputs.

Do not generate another aspect ratio and crop afterward.

---

# Protected Source Asset Rule

Uploaded brand logos and product PNGs are protected source assets.

The design must adapt around these assets.

Do not alter the assets to make them fit the design.

---

# Atomic Brand Logo Rule

Treat the uploaded logo as one indivisible graphic.

Everything visible inside the uploaded logo is protected logo artwork, including:

- symbol;
- emblem;
- wordmark;
- letters;
- brand-name text;
- spacing;
- internal alignment;
- colors;
- transparency;
- antialiased edges.

Text embedded inside the logo is NOT editable text.

Do not:

- OCR the wordmark and re-typeset it;
- regenerate logo letters;
- replace the wordmark with ordinary text;
- normalize or “correct” typography;
- alter character shapes;
- alter letter spacing or weight;
- change symbol-to-wordmark spacing;
- separate symbol and wordmark;
- rebuild the logo from generated elements.

Allowed complete-logo operations only:

- proportional scaling;
- positioning.

---

# Logo Placement Rule

Logo may appear only in the upper-left safe area.

For a 1200 × 1600 px canvas:

- minimum left clearance: 60 px
- minimum top clearance: 80 px

The complete logo must remain inside the canvas.

Logo position is not a candidate-composition variable.

---

# Logo Size Rule

Maximum logo bounding box:

- width: 220 px
- height: 100 px

Preserve the original aspect ratio.

Do not stretch, compress, crop, or distort.

Across master candidates:

- keep logo visual size consistent.

After master selection:

- logo position is locked;
- logo width is locked;
- logo height is locked.

---

# Information Zone Rule

The logo, product name, and version text form one stable information zone.

## Position

- logo remains in the upper-left safe area;
- product name appears below the logo;
- product name and version text must stay in the upper half of the canvas;
- the text block must not drift into the middle or lower half;
- center and lower areas should remain primarily available for product presentation.

## Alignment

Preferred alignment:

- product-name left edge aligns with the logo left edge whenever visually appropriate;
- version-text left edge aligns with the product-name left edge;
- logo, title, and version form one clear visual left axis.

If the logo shape makes mechanical alignment visually awkward, preserve the same visual left axis and balance without moving the logo away from the upper-left safe area.

## Spacing

Logo-to-title spacing must:

- provide clear breathing room;
- not feel cramped;
- not feel disconnected.

Title-to-version spacing must:

- remain visually stable;
- maintain clear hierarchy;
- keep both lines as one information group.

The information zone must not invade the product's core display area.

## Long Titles

For long product names:

- prefer one line;
- allow at most two lines;
- do not break words internally;
- moderately reduce title size if needed;
- keep the whole information zone in the upper half;
- do not push the text block downward into the image center.

## Master Lock

After master selection, lock:

- title position;
- version position;
- logo/title alignment relationship;
- logo-to-title spacing;
- title-to-version spacing;
- complete information-zone geometry.

All same-product variants must preserve these relationships.

---

# Product Protection Rule

The uploaded product PNG is the authoritative visual source.

Do not:

- redraw the product;
- approximate the product with a similar model;
- recolor the product;
- alter the silhouette;
- alter body/case/strap/earbud/charging-case shapes;
- alter buttons, crown, ports, holes, or hardware details;
- alter screen proportions;
- alter materials or finish;
- add nonexistent hardware;
- remove real details.

Allowed operations:

- proportional scaling;
- positioning;
- composition;
- natural contact shadow;
- restrained ambient shadow;
- subtle separation light.

---

# Visible Content Rule

Allowed visible content:

1. uploaded brand logo;
2. exact product name;
3. exact version text;
4. uploaded product PNG;
5. MD3 background geometry;
6. natural lighting and shadows.

Text naturally present on the uploaded product may remain.

Do not add:

- feature descriptions;
- specifications;
- promotions;
- discount labels;
- certifications;
- extra logos;
- extra icons;
- badges;
- decorative English words;
- marketplace stickers;
- invented interface elements.

---

# Typography Rule

Product name:

- modern neutral sans-serif;
- Google Sans / Roboto / Material-like visual language;
- Bold 700;
- prominent and readable;
- prefer one line;
- maximum two lines;
- do not shrink excessively.

Version:

- Medium 500;
- clearly readable;
- visually secondary to the product name;
- not tiny;
- not faint fine print.

---

# Lively MD3 Visual Direction

Use Material Design 3 as a visual language, not as an Android app interface.

Target mood:

- bright;
- light;
- lively;
- youthful;
- clean;
- breathable;
- modern;
- e-commerce friendly;
- premium without feeling heavy.

Use:

- rounded geometry;
- curves and partial circles;
- tonal surfaces;
- soft gradients;
- restrained depth;
- subtle elevation;
- generous whitespace;
- clear hierarchy.

Avoid:

- oppressive heavy-dark compositions;
- dated commercial poster mood;
- visually bulky pedestal scenes;
- theatrical black-studio treatment;
- excessive neon;
- aggressive bloom;
- movie fog;
- lens flare;
- unrealistic effects that alter the product.

---

# Adaptive Color System

Background color must be determined dynamically from the current product and the current composition.

There is no fixed default hue family.

Do not use a preset background-color table.

Every new product and every new master candidate should independently evaluate its own palette.

Evaluate:

- product luminance;
- product saturation;
- product material;
- visual weight;
- local accent colors visible on the product;
- brand visual presence;
- product/background separation;
- current composition;
- overall MD3 tonal balance;
- marketplace thumbnail readability.

Core principle:

**Use luminance and tonal separation to keep the product readable; allow hue to remain adaptive and free.**

Do not mechanically derive a background hue from product color.

Do not mechanically repeat a palette just because it worked for a previous product, candidate, or SKU.

---

# Dark Product Rule

If the product has low overall luminance:

Prioritize enough luminance separation between the product and the background so the silhouette remains clear at marketplace-thumbnail size.

Usually avoid making most of the canvas as dark as the product.

However:

- do not prescribe a specific background hue;
- do not force a predefined cool, warm, neutral, or pastel family;
- let the model choose the most suitable MD3 tonal palette for the current product and composition.

The requirement is clear separation and a lively commercial result, not a specific color.

---

# Light Product Rule

If the product has high overall luminance:

Ensure enough separation so the product does not visually disappear into the background.

Do not prescribe a specific background hue.

Let the model choose the most suitable MD3 tonal palette for the current product and composition.

The requirement is clear silhouette separation, not a preset color family.

---

# Colored Product Rule

For products with a clearly visible color:

Do not mechanically match the product hue.

Do not mechanically apply a complementary hue.

Choose the background palette freely according to:

- product appearance;
- material;
- visual weight;
- current composition;
- MD3 tonal balance;
- thumbnail clarity.

Hard requirements only:

- product and background remain clearly separated;
- the overall image remains modern, light, lively, and e-commerce friendly.

No fixed background-color list is used.

---

# Marketplace Thumbnail Rule

Design for product-card browsing first, not only standalone poster aesthetics.

At thumbnail size:

- product should be immediately recognizable;
- title should remain readable;
- product/background separation should remain clear;
- overall image should feel clean and clickable;
- the design should work naturally on a bright marketplace interface.

Do not sacrifice thumbnail clarity merely to create a dramatic poster effect.

---

# Pedestal / Platform Rule

A pedestal or platform is optional.

If used:

- keep it visually light;
- keep it subordinate to the product;
- avoid excessive thickness;
- avoid making it the visual weight center;
- use it only when it improves the composition.

The design may omit a pedestal entirely.

---

# Variant Color Adaptation

In REPLACE_VARIANT:

Keep the ORIGINAL MASTER geometry and layout locked.

The following may adapt to the current SKU:

- background main color;
- MD3 geometry fill colors;
- tonal-surface colors;
- shadow intensity;
- subtle separation light;
- text light/dark value only when contrast requires it.

Re-evaluate the palette for the CURRENT SKU.

Do not inherit the previous SKU palette as a preference.

Do not force all SKUs to share one background hue.

The goal is:

**same master structure, independently optimized MD3 palette for each SKU.**

---

# Variant Layout Lock

In REPLACE_VARIANT strictly preserve from Image A:

- logo artwork;
- logo size;
- logo position;
- product-name content;
- product-name size;
- product-name position;
- version content;
- version size;
- version position;
- title/version spacing;
- information-zone alignment;
- product display region;
- product visual-size logic;
- product visual center;
- background geometry shape;
- background geometry size;
- background geometry position;
- overall composition;
- primary lighting direction.

Do not redesign the poster.

---

# QA

For every output verify:

- strict 3:4 ratio;
- target 1200 × 1600;
- logo remains faithful to the uploaded logo;
- logo wordmark was not re-typeset;
- logo remains in upper-left safe area;
- logo stays within the maximum bounding box;
- product remains faithful to uploaded PNG;
- product was not redesigned or recolored;
- product name is exact;
- version text is exact;
- no extra text appears;
- no extra icons or badges appear;
- product name and version remain in the upper half;
- title remains below the logo;
- preferred left-alignment relationship is preserved;
- text does not invade the product's core display area;
- overall mood remains lively, modern, light, and marketplace friendly;
- product/background separation is clear at thumbnail size;
- background hue was selected adaptively rather than from a fixed preset.

For master candidates additionally verify:

- each candidate is a separate standalone image;
- no collage or grid is used;
- candidates differ meaningfully in composition;
- color was independently evaluated for each candidate;
- candidate palettes were not forced to differ merely for novelty.

For variants additionally verify:

- ORIGINAL MASTER is the source;
- logo did not move or resize;
- title/version did not move or resize;
- information-zone geometry did not change;
- product center and visual-size logic remain consistent;
- background geometry did not move, resize, or change shape;
- palette was re-evaluated for the current SKU rather than inherited from a previous variant.
