---
name: md3-product-main-image
description: >
  Create Google Material Design 3 inspired e-commerce product main images
  with GPT-image. Supports generating five master design candidates for a new
  product, selecting one approved master, replacing same-product color SKU
  variants while locking that master, and building complete multi-color SKU
  sets from the same original selected master.
---

# MD3 Product Main Image

## Purpose

Create premium 1200 × 1600 px e-commerce product main images for marketplaces
such as Ozon using GPT-image.

Each product receives its own independently designed master layout.

Different products do NOT need to share the same layout.

The only global consistency requirement across different products is:

- Google Material Design 3 inspired visual language
- strong marketplace readability
- protected uploaded assets
- clean product-first composition

For the SAME product with different colors:

1. Generate five master design candidates.
2. Wait for the user to select one.
3. Lock the selected candidate as the approved master.
4. Generate all remaining color SKUs from that ORIGINAL selected master.

Never independently redesign every color SKU.

---

# Workflow States

The workflow contains four states:

1. CREATE_MASTER_OPTIONS
2. SELECT_MASTER
3. REPLACE_VARIANT
4. BUILD_SKU_SET

Determine the correct state before generating images.

---

# STATE 1 — CREATE_MASTER_OPTIONS

Use when:

- this is a new product;
- there is no approved master;
- the user asks to create a product main image;
- the user asks to create a master;
- the user starts a new SKU set;
- the user asks to generate design options.

Generate exactly FIVE master design candidates.

All five candidates must use the SAME:

- uploaded brand logo;
- uploaded master product PNG;
- exact product name;
- exact version text;
- output size;
- MD3 design direction.

The five candidates must explore meaningfully different compositions.

Do NOT create five nearly identical images with only different background colors.

The candidates should differ in areas such as:

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

After generating the five candidates:

STOP.

Do not generate other color SKUs.

Wait for explicit user selection.

---

# Five Master Candidate Directions

The following are recommended design directions.

They are not rigid templates.

Adapt them to the actual product shape.

## Option 1 — Balanced Classic

- clear information zone;
- large product with balanced placement;
- restrained MD3 geometry;
- stable commercial composition.

## Option 2 — Product Dominant

- significantly larger product;
- reduced decorative geometry;
- strong marketplace-thumbnail readability;
- information zone carries less visual weight.

## Option 3 — Tonal Surface

- large rounded MD3 tonal surface;
- more visual layering;
- product interacts visually with the tonal field;
- controlled depth.

## Option 4 — Dynamic Arc

- stronger directional curve or arc;
- increased motion in the composition;
- strict text-protection zone;
- product remains dominant.

## Option 5 — Minimal Premium

- maximum negative space;
- minimal geometry;
- restrained tonal hierarchy;
- subtle studio lighting;
- premium high-end appearance.

The five designs must be genuinely different in layout and composition.

Changing only color does NOT count as a different design.

---

# STATE 2 — SELECT_MASTER

After five candidates exist, wait for the user to choose one.

Recognize selection language such as:

- 方案1
- 方案2
- 方案3
- 方案4
- 方案5
- 第一个
- 第二张
- 第3个
- 选4
- 用第五个
- 3号作为母版
- 第三张作为母版
- 就用这张
- 这张确认
- 这张作为母版

If selection is unambiguous:

MASTER_SELECTED = selected option

MASTER_APPROVED = true

The selected ORIGINAL image becomes the only master reference for later SKU
generation.

Do not merge several candidate designs.

Do not borrow elements from rejected options unless the user explicitly asks.

---

# Redesign Request

If the user says:

- 重新生成5个方案
- 这5个都不合适
- 再给我5个
- 重新设计母版
- 换一批方案
- 再做五个不同方案

return to:

CREATE_MASTER_OPTIONS

Generate a new set of five candidates.

Do not continue SKU production until the user selects a new master.

---

# STATE 3 — REPLACE_VARIANT

Use only after:

MASTER_APPROVED = true

The task is a locked-master product replacement.

Image A:

the ORIGINAL selected approved master.

Image B:

the new same-product color SKU PNG.

Do NOT create a new poster.

Do NOT reinterpret the composition.

Strictly preserve:

- brand logo visual size;
- brand logo location;
- product-name typography;
- product-name size;
- product-name position;
- version typography;
- version size;
- version position;
- title/version spacing;
- text alignment;
- product display area;
- product visual size;
- product visual center;
- background geometry shape;
- background geometry size;
- background geometry position;
- overall composition;
- main lighting direction.

Allowed changes:

- replacement product PNG;
- background main color;
- MD3 geometry color;
- shadow strength;
- subtle separation lighting;
- text light/dark value only where required for contrast.

The result should look like:

the same design file with a different product SKU inserted.

It should NOT look like:

a newly redesigned but similar poster.

---

# STATE 4 — BUILD_SKU_SET

Use when:

- the user uploads multiple color variants of the same product;
- the user asks for all SKUs;
- the user asks for a complete color set;
- the user asks for batch generation.

The workflow MUST be:

1. Identify the master SKU color.
2. Run CREATE_MASTER_OPTIONS for that SKU.
3. Generate exactly five master candidates.
4. STOP.
5. Wait for user selection.
6. Run SELECT_MASTER.
7. Lock the selected option.
8. Generate every remaining SKU using REPLACE_VARIANT.

Do not generate the full SKU set before master selection.

---

# Critical Batch Rule

Every SKU must be derived from the SAME ORIGINAL selected master.

Correct:

MASTER + SKU 2
MASTER + SKU 3
MASTER + SKU 4
MASTER + SKU 5

Incorrect:

MASTER → SKU 2 → SKU 3 → SKU 4

Never use a previously generated variant as the source for the next variant.

Always return to the ORIGINAL MASTER.

This reduces cumulative layout drift.

---

# Required Inputs

## CREATE_MASTER_OPTIONS

Required:

- uploaded brand logo;
- uploaded product PNG;
- product name;
- version text.

Optional:

- user-selected master color;
- additional same-product PNGs for product recognition only.

If multiple colors are uploaded and the user explicitly identifies the master
color, use that color.

If the user has not specified a master color, prefer the variant with:

- clear silhouette;
- strong edge separation;
- neutral visual balance.

Do not ask unnecessary questions when the correct choice is obvious.

---

## REPLACE_VARIANT

Required:

- approved selected master image;
- new same-product product PNG.

Do not proceed if there is no usable approved master.

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

# Uploaded Asset Protection

The uploaded brand logo and uploaded product PNG are PROTECTED SOURCE ASSETS.

They must be treated as authoritative visual assets.

The task is to design:

- layout;
- MD3 background;
- composition;
- lighting;
- shadow;
- visual hierarchy

AROUND the uploaded assets.

The task is NOT to redesign the uploaded assets themselves.

---

# Brand Logo Protection

Do NOT modify the uploaded brand logo.

This includes:

- do not redraw it;
- do not restyle it;
- do not reinterpret it;
- do not simplify it;
- do not embellish it;
- do not add effects that alter its original visual identity;
- do not distort it;
- do not stretch it;
- do not recolor it;
- do not change its internal proportions;
- do not replace it with a similar logo;
- do not generate a new logo inspired by it;
- do not convert it into a 3D object;
- do not add bevels, metallic effects, glow, outlines, shadows, or other
  stylization that changes its appearance unless the uploaded logo itself
  already contains them.

The uploaded logo must remain visually faithful to the original source.

Allowed operations:

- placement;
- proportional scaling;
- compositional positioning only.

The logo's internal artwork must remain unchanged.

---

# Product Image Protection

Do NOT modify the uploaded product image itself.

Treat the uploaded product PNG as the authoritative product reference.

Do NOT:

- redesign the product;
- redraw the product;
- reinterpret the product;
- change the product model;
- change the silhouette;
- change the case shape;
- change the strap shape;
- change the strap holes;
- change buttons;
- change crown design;
- change ports;
- change hardware details;
- change screen proportions;
- change physical materials;
- change surface finish;
- change product color;
- invent missing hardware;
- remove visible hardware details;
- add new physical details;
- stylize the product into another visual style;
- replace the uploaded product with an approximate generated substitute;
- create a product that merely looks similar to the uploaded PNG.

The generated result must remain visually faithful to the uploaded product PNG.

Allowed operations:

- proportional scaling;
- positioning;
- compositional placement;
- integration into the MD3 environment;
- natural lighting;
- realistic contact shadow;
- realistic ambient shadow;
- subtle separation light;
- same-product color SKU replacement using the uploaded SKU PNG.

Do NOT deform the product merely to fit the composition.

The composition must adapt to the product.

The product must not adapt structurally to the composition.

---

# Protected Asset Priority

If there is any conflict between:

- layout;
- decorative geometry;
- visual effect;
- creative styling;

and the fidelity of the uploaded logo or product PNG:

ASSET FIDELITY HAS PRIORITY.

Never sacrifice product or logo fidelity for visual creativity.

---

# Allowed Visible Content

Outside text naturally present inside the uploaded product render or screen,
the generated image may contain ONLY:

1. uploaded brand logo;
2. exact product name;
3. exact version text;
4. uploaded product PNG;
5. MD3-inspired background geometry;
6. natural lighting and shadows.

Do NOT add:

- feature descriptions;
- specification text;
- selling points;
- promotional copy;
- discount labels;
- certification marks;
- extra logos;
- extra icons;
- badges;
- decorative English words;
- invented UI;
- marketplace stickers;
- artificial labels.

Text naturally visible inside the uploaded product itself may remain.

---

# Canvas

Target:

1200 × 1600 px

Aspect ratio:

3:4

The image must remain suitable for Ozon-style marketplace thumbnails.

Keep critical information away from extreme edges.

---

# Visual Priority

Preferred hierarchy:

1. Product
2. Product name
3. Version
4. Brand logo
5. Background decoration

The product must remain the primary visual subject.

Decorative geometry must never overpower the product.

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

If the product name is long:

1. first try a readable one-line layout;
2. moderately reduce font size;
3. if still necessary, use maximum two lines.

Do not excessively shrink the title.

Do not break words internally.

Use semantic line breaks.

Example:

Xiaomi Smart Band 11
Active

is acceptable.

---

## Version

Use:

- modern neutral sans-serif;
- Medium;
- approximately weight 500.

Version text must remain clearly visible.

It should be visually secondary to the product name but must NOT look like
fine print.

Do NOT use:

- Light 300;
- extremely low opacity;
- very small subtitle typography;
- very pale gray simply to weaken the version.

Hierarchy should primarily come from:

Product Name = Bold 700

Version = Medium 500

---

# Information Layout

The brand logo, product name, and version form one information hierarchy.

Different products may use different layouts.

Do NOT force all products into the same universal template.

The composition may respond to:

- product silhouette;
- product-name length;
- product viewing angle;
- product visual weight;
- product color;
- available negative space.

The information hierarchy must remain readable.

Background decoration must adapt around the information zone.

The information zone must not adapt around decorative clutter.

---

# Background Geometry

Use restrained Google Material Design 3 inspired geometry.

Allowed examples:

- large arcs;
- partial circles;
- rounded tonal fields;
- rounded panels;
- curved surfaces;
- subtle gradients;
- layered tonal shapes.

Strong geometric edges must avoid:

- logo;
- product name;
- version text.

If geometry conflicts with information:

1. move geometry;
2. resize geometry;
3. simplify geometry.

Never reduce text readability merely to preserve a decorative shape.

---

# MD3 Design Direction

The image should communicate MD3 through:

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

This is a commercial product visual inspired by MD3.

---

# Product Priority

The product must:

- occupy substantial visual area;
- remain recognizable at marketplace thumbnail size;
- maintain correct proportions;
- have clear edge separation;
- receive realistic restrained lighting.

Do not make the product unnecessarily small to preserve decorative elements.

---

# Lighting

Use premium restrained studio lighting.

Allowed:

- controlled key light;
- subtle highlight;
- soft ambient light;
- realistic contact shadow;
- soft ambient shadow;
- subtle edge separation light where required.

Do NOT use:

- excessive bloom;
- dramatic lens flare;
- cinematic fog;
- aggressive neon;
- unrealistic reflections;
- effects that visually alter the actual product.

Lighting may enhance the product.

Lighting must not change product identity.

---

# Color System

Different same-product SKU colors may use different coordinated MD3 theme
colors.

The background color does NOT need to remain identical.

However:

the layout remains locked.

## Dark Product

Preferred themes:

- graphite;
- charcoal;
- dark cool gray;
- differentiated dark neutral surfaces.

Maintain clear separation from a black or dark product.

---

## Light / Colored Product

Preferred themes:

- cool gray;
- warm gray;
- muted neutral;
- restrained complementary color.

Avoid backgrounds that are too similar in hue and brightness to the product.

---

## White Product

Do NOT place white products on nearly white backgrounds.

Prefer:

- greige;
- taupe;
- stone;
- beige-gray;
- warm gray;
- muted cool gray.

Maintain clear silhouette separation.

---

## Pastel Product

For pink, light blue, cream, or other pastel products:

Do not simply match the background to the product color.

Use a related but sufficiently separated tonal palette.

The product must remain visually distinct.

---

# MASTER LOCK

Once a candidate is selected and approved, lock its visual structure.

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
- overall composition;
- primary light direction.

Allowed SKU-specific changes:

- uploaded replacement product PNG;
- background main color;
- background geometry color;
- shadow strength;
- subtle separation lighting;
- text light/dark value only where required for contrast.

Do NOT modify:

- master layout;
- typography geometry;
- composition;
- product placement logic;
- background geometry structure.

---

# CREATE_MASTER_OPTIONS Procedure

When state = CREATE_MASTER_OPTIONS:

1. Inspect the uploaded logo.
2. Inspect the uploaded master product PNG.
3. Protect both assets from modification.
4. Analyze product silhouette.
5. Analyze dominant product color.
6. Analyze product-name length.
7. Design five distinct MD3 compositions.
8. Use the exact uploaded product asset faithfully in all five.
9. Use the exact uploaded logo faithfully in all five.
10. Generate exactly five candidate master images.
11. Run Five-Option QA.
12. STOP.
13. Wait for user selection.

Do not automatically continue to SKU generation.

---

# SELECT_MASTER Procedure

When the user selects a candidate:

1. Identify the selected option.
2. Mark it as MASTER_SELECTED.
3. Mark MASTER_APPROVED = true.
4. Lock the ORIGINAL selected candidate.
5. Discard other candidates from production use.
6. If this is part of BUILD_SKU_SET, continue with remaining SKUs.

Do not redesign the selected master.

---

# REPLACE_VARIANT Procedure

When state = REPLACE_VARIANT:

1. Use the ORIGINAL approved master as Image A.
2. Use the uploaded replacement SKU PNG as Image B.
3. Treat Image B as a protected source asset.
4. Do NOT redesign Image B.
5. Replace the master product with the uploaded new SKU.
6. Preserve the same visual scale.
7. Preserve the same visual center.
8. Preserve the same placement logic.
9. Preserve logo and typography.
10. Preserve background geometry structure.
11. Adapt only allowed theme colors and shadow strength.
12. Run Variant QA.

Never use a previously generated variant as Image A.

Always use the ORIGINAL MASTER.

---

# BUILD_SKU_SET Procedure

When state = BUILD_SKU_SET:

## Phase 1 — Master Exploration

1. Identify the user-selected master SKU color.
2. Use that SKU PNG as the protected master product asset.
3. Generate exactly five CREATE_MASTER_OPTIONS.
4. STOP.
5. Wait for user selection.

Do not generate remaining SKUs before the user selects a master.

## Phase 2 — Master Lock

1. User selects one option.
2. Mark it MASTER_APPROVED.
3. Use that ORIGINAL selected image as the only master source.

## Phase 3 — SKU Production

For each remaining uploaded SKU:

Image A = ORIGINAL MASTER

Image B = uploaded SKU PNG

Generate using REPLACE_VARIANT.

Always:

MASTER + SKU 2
MASTER + SKU 3
MASTER + SKU 4
MASTER + SKU N

Never:

MASTER → SKU 2 → SKU 3 → SKU 4

This avoids cumulative layout drift.

---

# Five-Option QA

Before presenting the five candidates, verify:

- all five use the correct uploaded logo;
- the logo itself has not been modified;
- all five use the correct uploaded product;
- the product itself has not been redesigned;
- all five use the exact product name;
- all five use the exact version text;
- none contains extra marketing text;
- none contains invented badges;
- all are clearly MD3-inspired;
- all work as Ozon-style main images;
- product remains the primary visual subject;
- product/background separation is sufficient;
- typography is readable;
- version remains prominent;
- the five compositions are meaningfully different.

If two candidates differ mainly by color but not composition, regenerate one.

---

# Asset Fidelity QA

For EVERY generated image verify:

## Logo

- uploaded logo remains visually unchanged;
- logo color matches uploaded source;
- logo proportions match uploaded source;
- logo artwork has not been redrawn;
- logo has not been stylized;
- no approximate substitute logo appears.

## Product

- product matches uploaded product PNG;
- product model matches uploaded source;
- product color matches uploaded source;
- product silhouette matches uploaded source;
- product structure matches uploaded source;
- strap/body/case details match uploaded source;
- buttons/crown/hardware details match uploaded source;
- product has not been redesigned;
- no approximate generated substitute is used.

If the logo or product looks regenerated rather than faithfully preserved,
the image is incorrect.

Regenerate with stronger asset-protection instructions.

---

# Variant QA

Compare every variant directly with the ORIGINAL approved master.

Verify:

- logo has not visibly moved;
- logo has not visibly resized;
- logo artwork remains unchanged;
- title has not visibly moved;
- title has not visibly resized;
- version has not visibly moved;
- version has not visibly resized;
- title/version spacing remains consistent;
- product visual scale remains consistent;
- product visual center remains consistent;
- product physical appearance exactly matches the uploaded SKU;
- geometry remains structurally identical;
- geometry has not visibly moved or resized;
- no additional text appears.

If the result looks like a new poster:

reject it.

Regenerate as a stricter locked-master replacement.

---

# SKU Set QA

When all color SKUs are complete, compare them as one sequence.

They should feel like:

SAME MASTER
+
DIFFERENT UPLOADED PRODUCT SKU
+
ADAPTIVE MD3 COLOR THEME

They should NOT feel like:

independently designed posters.

They should also NOT contain modified versions of the uploaded product.

---

# User Approval State

If the user says:

- 方案3
- 选第三个
- 第三张作为母版
- 就用这个
- 这张确认
- 这张做母版
- 这个方案可以
- 锁定这个方案

and the reference is unambiguous:

set:

MASTER_APPROVED = true

From that point onward:

all same-product SKUs must use the selected ORIGINAL master.

Do not return to CREATE_MASTER_OPTIONS unless the user explicitly asks to
redesign or regenerate the five options.

---

# Highest Priority Rule

Uploaded brand logo fidelity and uploaded product image fidelity are mandatory.

If any instruction conflicts with asset fidelity:

asset fidelity wins.

The design must adapt around the uploaded assets.

The uploaded assets must not be redesigned to fit the design.
