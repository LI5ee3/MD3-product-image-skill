---
name: md3-product-main-image
description: >
  GPT-image-only workflow for creating premium Google Material Design 3 inspired
  e-commerce product main images. Generates five master candidates for a new
  product, waits for user selection, locks the selected master, and creates
  same-product SKU variants from that original master while protecting uploaded
  logos and product PNGs from redesign or alteration.
---

# MD3 Product Main Image

## Purpose

Create premium e-commerce product main images for marketplaces such as Ozon using GPT-image.

Each product receives its own independent master layout. Different products do not need to share the same composition.

For the SAME product with different colors:

1. Generate five master candidates.
2. Wait for the user to select one.
3. Lock the selected candidate as the approved master.
4. Generate every remaining SKU from that ORIGINAL selected master.

Never independently redesign every color SKU.

# Highest Priority Rules

## Uploaded Asset Protection

The uploaded brand logo and uploaded product PNG are PROTECTED SOURCE ASSETS.

They are authoritative visual assets. Do NOT redraw, redesign, reinterpret, recolor, restyle, distort, restructure, or replace them with approximate generated substitutes.

The design must adapt around the uploaded assets. The uploaded assets must NOT be altered to fit the design.

## Same-Product Master Lock

Once a master candidate is selected, all same-product SKU variants must use the ORIGINAL selected master as Image A.

Never redesign the layout for another color SKU. Never use a generated variant as the source for the next variant.

## No Extra Content

Outside text naturally visible inside the uploaded product render/screen, the image may contain ONLY:

- uploaded brand logo;
- exact product name;
- exact version text;
- uploaded product PNG;
- MD3-inspired background geometry;
- natural lighting and shadows.

Do NOT add selling points, specifications, promotional copy, discounts, badges, certification marks, extra logos, extra icons, decorative English words, invented UI, marketplace stickers, or artificial labels.

# Workflow States

1. CREATE_MASTER_OPTIONS
2. SELECT_MASTER
3. REPLACE_VARIANT
4. BUILD_SKU_SET

# STATE 1 — CREATE_MASTER_OPTIONS

Use when this is a new product, there is no approved master, the user asks for a new master, or the user asks for a fresh set of options.

Generate exactly FIVE master candidates.

All five must use the SAME uploaded logo, SAME uploaded master product PNG, SAME product name, SAME version text, SAME canvas size, and SAME MD3 design direction.

The five candidates must be meaningfully different in composition. Changing only background color does NOT count.

Explore meaningful differences in:

- product placement;
- product scale;
- information-zone placement;
- negative-space distribution;
- MD3 geometry;
- arc position;
- tonal surface structure;
- depth;
- lighting balance;
- overall composition.

After generating the five candidates: STOP. Do not generate other SKUs. Wait for explicit user selection.

# Master Candidate Diversity Requirement

The five master candidates must be genuinely different in composition.

They must NOT be five versions of the same layout with only different colors.

Explore meaningful differences in:

- product placement;
- product visual scale;
- information-zone placement;
- negative-space distribution;
- MD3 geometry structure;
- arc / curve placement;
- tonal surface arrangement;
- spatial depth;
- lighting balance;
- overall visual rhythm.

Do not force any predefined composition categories.

The five candidates should be designed freely according to the actual product
silhouette, viewing angle, product-name length, product color, and visual weight.

# STATE 2 — SELECT_MASTER

After five candidates exist, wait for the user to choose one.

Recognize unambiguous selections such as:

- 方案1 / 方案2 / 方案3 / 方案4 / 方案5
- 第一个 / 第二张 / 第3个
- 选4 / 用第五个
- 3号作为母版 / 第三张作为母版
- 就用这张 / 这张确认 / 锁定这个方案

When selection is unambiguous:

MASTER_SELECTED = selected option
MASTER_APPROVED = true

The selected ORIGINAL candidate becomes the ONLY production master.

Do not mix or borrow composition elements from rejected candidates unless explicitly requested.

If the user merely comments on an option without selecting it, do not lock it. Example: “3的颜色不错” is not necessarily approval; “方案3不错，就用这个” is approval.

# Redesign Request

If the user says “重新生成5个方案”, “这5个都不合适”, “再给我5个”, “重新设计母版”, or equivalent, return to CREATE_MASTER_OPTIONS and generate a fresh set of five. Do not continue SKU production until a new master is selected.

# STATE 3 — REPLACE_VARIANT

Use only after MASTER_APPROVED = true.

Image A = ORIGINAL selected approved master.
Image B = uploaded replacement same-product SKU PNG.

This is a locked-master product replacement, NOT a new poster design.

Strictly preserve from Image A:

- brand logo visual size and location;
- product-name typography, size, and location;
- version typography, size, and location;
- title/version spacing;
- text alignment;
- product display area;
- product visual size;
- product visual center;
- background geometry shape, size, and location;
- overall composition;
- main lighting direction.

Allowed changes only:

- replacement product PNG;
- background main color;
- MD3 geometry color;
- shadow strength;
- subtle separation lighting;
- text light/dark value only when required for contrast.

The result should look like the same master with another uploaded SKU inserted.

# STATE 4 — BUILD_SKU_SET

Use when the user uploads multiple colors of the same product and asks for a complete SKU set.

Workflow MUST be:

1. Identify the master SKU color.
2. Run CREATE_MASTER_OPTIONS for that SKU.
3. Generate exactly five master candidates.
4. STOP.
5. Wait for user selection.
6. Run SELECT_MASTER.
7. Lock the selected ORIGINAL candidate.
8. Generate every remaining SKU using REPLACE_VARIANT.

Do not generate the full SKU set before the user selects a master.

# Critical Batch Rule

Correct:

MASTER + SKU 2
MASTER + SKU 3
MASTER + SKU 4
MASTER + SKU N

Incorrect:

MASTER → SKU 2 → SKU 3 → SKU 4

Every variant must always derive from the SAME ORIGINAL selected master to reduce cumulative layout drift.

# Required Inputs

## CREATE_MASTER_OPTIONS

Required:

- uploaded brand logo;
- uploaded product PNG;
- product name;
- version text.

Optional:

- user-selected master color;
- additional same-product PNGs for recognition only.

If multiple colors are uploaded and the user explicitly identifies the master color, use it. If not specified, prefer the variant with the clearest silhouette and strongest neutral visual balance.

## REPLACE_VARIANT

Required:

- approved selected master image;
- new same-product uploaded SKU PNG.

## BUILD_SKU_SET

Required:

- brand logo;
- product name;
- version text;
- at least two same-product color PNGs.

# Brand Logo Protection

Do NOT modify the uploaded logo.

Forbidden:

- redraw;
- recolor;
- restyle;
- reinterpret;
- simplify;
- embellish;
- distort/stretch;
- change internal proportions;
- replace with a similar logo;
- generate a new logo inspired by it;
- 3D conversion;
- bevel/metal/glow/outline/effects that alter identity.

Allowed only:

- proportional scaling;
- placement;
- compositional positioning.

The logo artwork itself must remain visually unchanged.

# Product Image Protection

Treat every uploaded product PNG as the authoritative product asset.

Do NOT:

- redesign or redraw the product;
- change the product model;
- change silhouette;
- change case/body shape;
- change strap shape or holes;
- change buttons/crown/ports/hardware details;
- change screen proportions;
- change materials or finish;
- change product color;
- invent/remove hardware details;
- stylize the product into another visual style;
- replace it with an approximate generated substitute.

Allowed only:

- proportional scaling;
- positioning;
- compositional placement;
- natural integration into the MD3 environment;
- realistic contact/ambient shadows;
- subtle separation light;
- same-product SKU replacement using the uploaded SKU PNG.

Do NOT deform the product merely to fit the composition.

The composition must adapt to the product. The product must not adapt structurally to the composition.

# Asset Fidelity Priority

If layout, geometry, lighting, or creative styling conflicts with uploaded-asset fidelity, ASSET FIDELITY WINS.

# Canvas

- Target: 1200 × 1600 px
- Aspect ratio: 3:4
- Optimized for Ozon-style marketplace thumbnails.

# Visual Priority

1. Product
2. Product name
3. Version
4. Brand logo
5. Background decoration

The product must remain the primary visual subject.

# Typography

## Product Name

- modern neutral sans-serif;
- Material / Roboto / Google Sans inspired;
- Bold 700;
- highly visible;
- prefer one line;
- maximum two lines if needed;
- never split words internally;
- do not excessively shrink long names.

## Version

- modern neutral sans-serif;
- Medium 500;
- clearly visible;
- visually secondary to title but not faint fine print.

# Information Layout

Logo, product name, and version form one information hierarchy.

Different products may use different layouts. Do not force all products into one universal template.

Background decoration must adapt around the information zone and never reduce readability.

# Background Geometry

Allowed MD3-inspired geometry includes:

- large arcs;
- partial circles;
- rounded tonal fields;
- rounded panels;
- curved surfaces;
- subtle gradients;
- layered tonal shapes.

Strong geometry must avoid logo, title, and version text.

If geometry conflicts with text: move, resize, or simplify geometry.

# MD3 Design Direction

Use:

- rounded geometry;
- tonal surfaces;
- adaptive color;
- subtle elevation;
- clean hierarchy;
- generous spacing;
- restrained depth;
- soft gradients;
- large simple forms.

Do NOT make the image look like an Android application UI.

# Lighting

Use restrained premium studio lighting.

Allowed:

- controlled key light;
- subtle highlight;
- soft ambient light;
- realistic contact shadow;
- soft ambient shadow;
- subtle edge separation light.

Do NOT use excessive bloom, dramatic lens flare, cinematic fog, aggressive neon, unrealistic reflections, or effects that alter product identity.

# Color System

Different same-product SKU colors may use different coordinated MD3 theme colors while layout remains locked.

Dark products:

- graphite;
- charcoal;
- dark cool gray;
- differentiated dark neutrals.

Light/colored products:

- cool gray;
- warm gray;
- muted neutral;
- restrained complementary color.

White products:

- never near-white background;
- prefer greige, taupe, stone, beige-gray, warm gray, muted cool gray.

Pastel products:

- avoid backgrounds too similar in hue and brightness;
- maintain clear product separation.

# MASTER LOCK

Once a candidate is selected, lock:

- logo visual size/location;
- product-name size/location;
- version size/location;
- title/version spacing;
- text alignment;
- product display area;
- product visual size/center;
- background geometry shape/size/location;
- overall composition;
- primary light direction.

Allowed per SKU only:

- uploaded replacement product PNG;
- background main color;
- background geometry color;
- shadow strength;
- subtle separation lighting;
- text light/dark value for contrast.

# CREATE_MASTER_OPTIONS Procedure

1. Inspect uploaded logo.
2. Inspect uploaded master product PNG.
3. Protect both assets from modification.
4. Analyze silhouette, color, text length, and visual weight.
5. Design five distinct MD3 compositions.
6. Use the uploaded product faithfully in all five.
7. Use the uploaded logo faithfully in all five.
8. Generate exactly five candidate master images.
9. Run Five-Option QA.
10. STOP and wait for user selection.

# SELECT_MASTER Procedure

1. Identify selected option.
2. Mark MASTER_SELECTED.
3. Set MASTER_APPROVED = true.
4. Lock the ORIGINAL selected candidate.
5. Discard other candidates from production use.
6. If in BUILD_SKU_SET, continue with remaining SKUs.

# REPLACE_VARIANT Procedure

1. Use ORIGINAL approved master as Image A.
2. Use uploaded replacement SKU PNG as Image B.
3. Treat Image B as protected.
4. Do NOT redesign Image B.
5. Replace the master product with Image B.
6. Preserve visual scale, center, and placement logic.
7. Preserve logo and typography.
8. Preserve background geometry structure.
9. Adapt only allowed theme colors and shadow strength.
10. Run Variant QA.

# BUILD_SKU_SET Procedure

## Phase 1 — Master Exploration

1. Identify master SKU color.
2. Use its uploaded PNG as protected master asset.
3. Generate exactly five master candidates.
4. STOP.
5. Wait for user selection.

## Phase 2 — Master Lock

1. User selects one option.
2. Mark MASTER_APPROVED.
3. Use that ORIGINAL selected image as the only master source.

## Phase 3 — SKU Production

For each remaining uploaded SKU:

Image A = ORIGINAL MASTER
Image B = corresponding uploaded SKU PNG

Generate using REPLACE_VARIANT.

# Five-Option QA

Verify:

- correct uploaded logo in all five;
- logo itself unchanged;
- correct uploaded product in all five;
- product itself not redesigned;
- exact product name;
- exact version text;
- no extra marketing text/badges;
- all clearly MD3-inspired;
- all suitable for 1200 × 1600 Ozon main images;
- product dominant;
- sufficient product/background separation;
- readable typography;
- five compositions meaningfully different.

If two candidates differ mainly by color, regenerate one with a genuinely different composition.

# Asset Fidelity QA

For EVERY image verify:

## Logo

- logo artwork unchanged;
- logo color matches upload;
- logo proportions match upload;
- no stylized or approximate substitute.

## Product

- model matches uploaded PNG;
- color matches uploaded PNG;
- silhouette matches uploaded PNG;
- structure/details match uploaded PNG;
- no redesign;
- no approximate generated substitute.

If logo or product looks regenerated rather than faithfully preserved, reject and regenerate with stronger asset-protection instructions.

# Variant QA

Compare every variant directly with ORIGINAL approved master.

Verify:

- logo does not move/resize/change artwork;
- title does not move/resize;
- version does not move/resize;
- title/version spacing remains consistent;
- product scale/center remains consistent;
- product physical appearance matches uploaded SKU;
- geometry remains structurally identical and does not move/resize;
- no additional text appears.

If the result looks like a new poster, reject and regenerate as a stricter locked-master replacement.

# Final Principle

Uploaded logo fidelity and uploaded product fidelity are mandatory.

If any instruction conflicts with asset fidelity: ASSET FIDELITY WINS.
