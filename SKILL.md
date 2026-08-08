---
name: md3-product-main-image
description: >
  GPT-image-only workflow for creating premium MD3 e-commerce product main images.
  Generates five master candidates as five SEPARATE image outputs, one at a time,
  waits for user selection, then locks the selected original master for single or
  batch SKU replacement while protecting uploaded logos and product images.
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

#

# Atomic Brand Logo Rule

The uploaded brand logo must be treated as ONE INDIVISIBLE raster graphic.

Everything visible inside the uploaded logo image is part of the protected
logo artwork, including:

- symbol;
- icon;
- emblem;
- wordmark;
- letters;
- brand-name text;
- spacing;
- internal alignment;
- color;
- transparency;
- anti-aliased edges.

Do NOT interpret any letters, words, or characters inside the uploaded logo
as editable text.

Do NOT:

- OCR the logo wordmark and typeset it again;
- regenerate letters using a font;
- replace the wordmark with ordinary text;
- correct or normalize the typography;
- change letter spacing;
- change character shapes;
- change wordmark weight;
- change the relationship between symbol and wordmark;
- separate the symbol from the wordmark;
- reconstruct the logo from multiple generated elements.

For example, if an uploaded HUAWEI logo contains both the flower symbol and
the word "HUAWEI", the word "HUAWEI" is part of the protected logo artwork.

It is NOT editable text.

The complete uploaded logo image must be treated as one atomic visual asset.

Allowed operations on the complete logo asset are ONLY:

- proportional scaling of the entire logo;
- positioning of the entire logo;
- placement inside the defined upper-left safe area.

Never reconstruct individual parts of the logo.

---

# Logo Text Exclusion Rule

Text-generation and text-layout rules do NOT apply to text already embedded
inside the uploaded brand logo.

Any letters, words, numbers, or characters visible inside the uploaded logo
must remain part of the original logo graphic.

Do NOT:

- transcribe them;
- rewrite them;
- typeset them;
- translate them;
- correct them;
- normalize them;
- regenerate them;
- separate them from the logo graphic.

Only the user-provided product name and version text are editable/generated
text elements.

Text embedded inside the uploaded logo is never editable.

# Brand Logo Position Lock

The uploaded brand logo has a FIXED POSITION RULE.

The logo may appear ONLY in the UPPER-LEFT corner of the image.

It must remain fully inside the upper-left safe area.

For a 1200 × 1600 px canvas:

- keep at least 60 px clearance from the left edge;
- keep at least 80 px clearance from the top edge;
- keep the entire logo visually within the upper-left zone;
- do not place any part of the logo outside the canvas;
- do not place the logo at top-center, top-right, center, bottom, or any other location.

The logo must be top-left anchored in:

- all five master candidates;
- the selected approved master;
- every REPLACE_VARIANT output;
- every BUILD_SKU_SET output.

Background geometry must avoid the logo safe area.

The product name and version text must be arranged around the fixed logo zone,
not by moving the logo elsewhere.

The logo artwork itself remains protected and may only be proportionally scaled
and positioned within this upper-left safe area.


# Brand Logo Size Lock

The uploaded brand logo is size-controlled in addition to being position-locked.

For a 1200 × 1600 px canvas:

Maximum logo bounding box:

- width: 220 px;
- height: 100 px.

The logo must preserve its original aspect ratio.

Do NOT:

- stretch the logo;
- compress the logo;
- crop the logo;
- distort the logo;
- force it to fill the entire bounding box;
- resize it merely to create visual variety between master candidates.

Recommended visual target:

- horizontal logos should normally occupy approximately 10%–18% of the canvas width;
- however, preserve the original logo proportions instead of forcing a fixed width.

The logo must remain clearly readable but visually subordinate to:

1. the product;
2. the product name.

## Five-Candidate Consistency

Across all five master candidates:

- logo position must remain in the same upper-left safe zone;
- logo visual size should remain consistent;
- logo scale must NOT be used as a composition variable.

The five candidates should differ through product placement, layout, negative
space, MD3 geometry, tonal surfaces, lighting, and visual balance — not through
changing the brand logo size.

## Locked Master Consistency

Once a master candidate is selected:

- logo width is locked;
- logo height is locked;
- logo position is locked.

All subsequent REPLACE_VARIANT and BUILD_SKU_SET outputs must preserve the same
logo visual size and position as the ORIGINAL MASTER.

Do not resize the logo according to SKU color, background color, or theme.

# Uploaded Asset Protection

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

# Separate Master Output Rule

The five master candidates must be generated as FIVE SEPARATE IMAGE OUTPUTS.

This is a hard rule.

NEVER place multiple candidates inside one image.

Do NOT create:

- contact sheets;
- collages;
- grids;
- mood boards;
- comparison boards;
- storyboards;
- multi-panel layouts;
- five-in-one layouts;
- thumbnail sheets.

Each master candidate must be its own complete standalone image.

Each standalone candidate must independently use:

- strict 3:4 aspect ratio;
- target size 1200 × 1600 px;
- one complete composition;
- one intact uploaded brand logo;
- one exact product name;
- one exact version text;
- one intact uploaded product PNG;
- one complete MD3 background composition.

Do NOT place option numbers such as:

- 01;
- 02;
- 03;
- 04;
- 05;
- Option 1;
- 方案1

inside the generated artwork.

Option numbers are conversation labels only.

## Sequential Generation Requirement

Generate the five candidates sequentially:

1. GENERATE_OPTION_1
2. GENERATE_OPTION_2
3. GENERATE_OPTION_3
4. GENERATE_OPTION_4
5. GENERATE_OPTION_5
6. WAIT_FOR_SELECTION

Each generation step produces exactly ONE standalone image.

After each image is generated, continue to the next option only if the interface
can reliably create another separate image output.

If the interface cannot reliably return five separate images in one response,
prioritize standalone output quality over quantity:

- generate Option 1 only;
- stop;
- wait for the user to say "continue" or request the next option.

Never solve this limitation by combining multiple candidates into one image.


# STATE 1 — CREATE_MASTER_OPTIONS

Use when:

- this is a new product;
- there is no approved master;
- the user asks to create a product main image;
- the user asks to create a master;
- the user asks for multiple design options;
- the user starts a new SKU set;
- the user explicitly asks to regenerate the master options.

The target is FIVE master candidates, but they must be generated as FIVE
SEPARATE standalone images, never as one combined image.

Generation sequence:

GENERATE_OPTION_1
→ one standalone 3:4 image

GENERATE_OPTION_2
→ one standalone 3:4 image

GENERATE_OPTION_3
→ one standalone 3:4 image

GENERATE_OPTION_4
→ one standalone 3:4 image

GENERATE_OPTION_5
→ one standalone 3:4 image

→ WAIT_FOR_SELECTION

All five candidates must use the SAME:

- uploaded brand logo;
- uploaded master product PNG;
- exact product name;
- exact version text;
- strict 3:4 ratio;
- target size 1200 × 1600 px;
- MD3 design direction;
- protected source assets.

The candidates must explore meaningfully different compositions.

Do NOT create five nearly identical images with only different background colors.

Do NOT create a collage/contact sheet/grid to display all five candidates.

After the fifth standalone candidate is generated:

STOP.

Do not generate other color SKUs.

Wait for explicit user selection.

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
2. Generate the five candidates sequentially as separate images.
3. Never combine them into one contact sheet, collage, grid, or multi-panel image.
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


# Information Zone Position and Alignment Rule

The brand logo, product name, and version text must form one stable information zone.

- Brand logo stays in the upper-left safe area.
- Product name must appear below the logo.
- Product name and version text must remain in the UPPER HALF of the canvas.
- Product-name left edge should align with the logo left edge whenever visually appropriate.
- Version-text left edge should align with the product-name left edge.
- Keep intentional vertical breathing room between logo and product name.
- Keep a stable, natural hierarchy gap between product name and version.
- The information zone must not invade the product's core display area.
- Long product names may use at most two lines and must still remain in the upper half.
- Do not push the information zone toward the center or lower half to solve layout conflicts.

Across all five master candidates, preserve the same upper-half information-zone logic.

After master selection, lock:
- title position;
- version position;
- logo/title left-alignment relationship;
- logo-to-title spacing;
- title-to-version spacing;
- complete information-zone geometry.

All same-product variants must preserve the ORIGINAL MASTER information zone.

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


# Atomic Logo QA

For EVERY generated image verify:

- the complete uploaded logo appears as one intact graphic;
- symbol and wordmark remain together exactly as uploaded;
- any text embedded inside the logo has NOT been re-typeset;
- letter shapes match the uploaded logo graphic;
- letter spacing matches the uploaded logo graphic;
- symbol-to-wordmark spacing remains unchanged;
- logo transparency and internal alignment remain faithful;
- no part of the logo has been reconstructed independently;
- no generated substitute wordmark appears.

If the model has regenerated the wordmark as editable text or reconstructed
any part of the logo, the output is incorrect.

Regenerate with stronger Atomic Brand Logo instructions.

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


# Lively MD3 Tone and Mood Rule

The visual language must use Material Design 3, but the MOOD must remain:

- lively;
- bright;
- light;
- youthful;
- clean;
- breathable;
- modern;
- e-commerce friendly;
- premium without feeling old or heavy.

This rule is especially important for dark products.

A dark product must NOT automatically result in a mostly black or oppressive image.

## Preferred mood

Aim for:

- soft tonal surfaces;
- brighter layered neutrals;
- light-to-mid gray structures;
- cool gray / blue-gray / stone-gray tonal depth;
- gentle contrast;
- open whitespace;
- clear product-background separation;
- fresh, contemporary energy.

## Avoid

Do NOT create an image that feels:

- too black;
- too dark;
- too heavy;
- too old-fashioned;
- too formal in a dated way;
- like a luxury dark showroom;
- like a heavy exhibition pedestal scene;
- like a black studio backdrop;
- like a dramatic premium poster instead of an e-commerce main image.

## Background restriction

Even for black or dark products:

- avoid large pure-black backgrounds;
- avoid turning most of the canvas into near-black;
- prefer gray, cool-gray, graphite-gray, blue-gray, mist-gray, or other lighter MD3 tonal combinations;
- ensure the overall image still feels bright enough and commercially attractive.

## Base / pedestal restriction

If a base, platform, or pedestal is used:

- it must stay visually light;
- it must not become the dominant visual weight of the composition;
- it must not feel thick, bulky, or heavy;
- prefer thinner, lighter, softer tonal-surface style bases;
- it may be omitted if it makes the image feel heavy.

## Geometry behavior

MD3 geometry must function as light layered visual structure,
not as a dark theatrical set.

Use:

- soft rounded surfaces;
- tonal layers;
- airy arcs;
- clean curved shapes;
- subtle elevation.

Avoid:

- oppressive dark masses;
- over-dominant dark arcs;
- visually heavy geometric blocks.

## Product priority

The product should remain the visual focus, but the overall scene should still
feel fresh and lively rather than dramatic and heavy.

## Variant consistency

This tone rule applies to:

- all master candidates;
- the selected master;
- all REPLACE_VARIANT outputs;
- all BUILD_SKU_SET outputs.


# Dark Product Background Priority Rule

For black or dark products, the preferred direction is a LIGHTER MD3 background,
not a darker one.

This is a high-priority e-commerce rule.

## Default preference for dark products

When the product itself is black, graphite, charcoal, dark gray, dark blue, or
otherwise visually dark, prefer:

- light cool gray;
- mist gray;
- pale blue-gray;
- soft neutral gray;
- stone gray;
- warm light gray;
- light-to-mid tonal-surface backgrounds.

Do NOT automatically assume that a dark product should be placed on a dark
background.

## Avoid for dark products

Unless the user explicitly requests a dark poster look, avoid:

- large black backgrounds;
- near-black canvases;
- very dark showroom scenes;
- heavy dark pedestal scenes;
- dark-on-dark low-separation compositions.

## E-commerce card logic

The goal is better visibility inside marketplace list cards.

Dark products should stand out through:

- clearer silhouette separation;
- brighter surrounding tonal surfaces;
- lighter, cleaner overall presentation;
- faster recognition in thumbnail browsing.

Do not sacrifice thumbnail readability merely to create a dramatic premium-dark look.

## Priority over mood ambiguity

If there is ambiguity between:

A) a dramatic dark premium poster look
and
B) a brighter, cleaner, more sellable marketplace image,

prefer B by default.


# Tone and Mood QA

For EVERY generated image verify:

- the image feels lively, bright, light, and modern;
- the image does not feel too black, too heavy, or old-fashioned;
- dark products are separated from the background without relying on large pure-black areas;
- the background uses MD3 tonal layering rather than a black studio look;
- any pedestal/base remains visually light and not dominant;
- the image feels suitable for e-commerce rather than a heavy luxury poster.


# Marketplace Thumbnail QA

For dark-product images verify:

- the product is clearly readable in thumbnail size;
- the background is bright enough for strong silhouette separation;
- the composition feels suitable for Ozon-style card browsing;
- the image is not relying on a mostly black backdrop;
- the product looks commercial and clickable rather than dark and heavy.
