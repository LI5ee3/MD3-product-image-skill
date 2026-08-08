# MD3 Product Main Image Skill v3.8

GPT-image-only workflow for creating Ozon-style e-commerce product main images.

This version does NOT use Photoshop, PSD automation, website integration, or
external compositing.
---

# Mood Update in v3.8

This version adds an explicit “lively MD3” mood rule.

The design must not only follow MD3 geometry, but also preserve a brighter,
lighter, younger, more breathable e-commerce mood.

This is especially important for dark products.

## Required mood

- bright
- light
- lively
- youthful
- clean
- fresh
- modern
- premium without feeling heavy

## Avoid

- large pure-black backgrounds
- overly dark compositions
- heavy exhibition pedestal feeling
- old-fashioned commercial poster tone
- luxury-dark showroom mood
- black studio backdrop look

## Practical interpretation

For black or dark products:

- do NOT automatically use a mostly black background;
- prefer brighter gray / cool-gray / blue-gray / graphite-gray tonal surfaces;
- keep the pedestal/base light, thin, and visually secondary;
- preserve product contrast without making the whole image oppressive.

---

# Black/Dark Product Update in v3.8

This version adds a stronger marketplace-first rule for black and dark products.

## Core rule

For black or dark products, prefer lighter MD3 backgrounds by default.

Recommended directions:

- light cool gray
- mist gray
- pale blue-gray
- soft neutral gray
- stone gray
- warm light gray

## Avoid by default

Unless the user explicitly asks for a dark-poster look, avoid:

- large black backgrounds
- near-black canvases
- dark-on-dark low-separation scenes
- heavy dark pedestals
- dark showroom moods

## Why

The purpose is to improve:

- thumbnail readability
- product silhouette separation
- Ozon-style list-card visibility
- commercial clickability

The image should be optimized for marketplace browsing, not only for standalone poster aesthetics.


---

# Core Workflow

For every new product:

1. Upload the brand logo.
2. Upload the product PNG chosen as the master SKU.
3. Provide the product name and version text.
4. Generate five master candidates as FIVE SEPARATE image outputs.
5. Review the five standalone images.
6. Select one option.
7. Lock that original image as ORIGINAL MASTER.
8. Generate every remaining color SKU directly from ORIGINAL MASTER.

Never generate five candidates inside one collage/contact sheet.

Never generate variants in a chain.

Correct:

ORIGINAL MASTER + SKU 2
ORIGINAL MASTER + SKU 3
ORIGINAL MASTER + SKU 4

Incorrect:

MASTER → SKU 2 → SKU 3 → SKU 4

---

# Master Candidate Output Rule

"Generate five master candidates" means:

- five independent image files;
- one design per image;
- one standalone 3:4 canvas per candidate.

Forbidden:

- contact sheet;
- collage;
- grid;
- mood board;
- comparison board;
- storyboard;
- multi-panel image;
- five designs inside one canvas.

Do not render option numbers such as 01, 02, 03, 04, 05 inside the artwork.

Option numbering belongs only to the conversation.

## Sequential Generation

Preferred sequence:

OPTION 1 → one standalone image  
OPTION 2 → one standalone image  
OPTION 3 → one standalone image  
OPTION 4 → one standalone image  
OPTION 5 → one standalone image  
→ wait for user selection

If the interface cannot reliably generate five separate images in one response:

- generate OPTION 1 only;
- stop;
- wait for the user to request OPTION 2;
- continue one image at a time.

Never replace separate outputs with a collage.

---

# Canvas Rules

Every generated image must use:

- strict aspect ratio: 3:4
- target size: 1200 × 1600 px

This applies to:

- all master candidates;
- selected master;
- single SKU variants;
- batch SKU outputs.

Do not generate another ratio first and crop afterward.

---

# Brand Logo Rules

The uploaded logo is a protected atomic visual asset.

## Atomic Logo

Treat the entire uploaded logo as ONE indivisible graphic.

This includes:

- symbol;
- emblem;
- wordmark;
- letters;
- brand-name text;
- spacing;
- colors;
- transparency.

Text embedded inside the logo is NOT editable text.

Do not:

- OCR and re-typeset it;
- regenerate the wordmark;
- change character shapes;
- change letter spacing;
- change font weight;
- separate symbol and wordmark;
- rebuild the logo;
- substitute a similar logo.

Only scale and position the entire logo as one unit.

## Logo Position

Logo may appear ONLY in the upper-left safe area.

For 1200 × 1600 px:

- minimum left margin: 60 px
- minimum top margin: 80 px

Logo must remain fully inside the canvas.

## Logo Size

Maximum bounding box:

- width: 220 px
- height: 100 px

Preserve original aspect ratio.

Do not stretch, compress, crop, or distort.

Across the five master candidates:

- logo location logic stays upper-left;
- logo visual size stays consistent.

After master selection:

- logo width is locked;
- logo height is locked;
- logo position is locked.

---

# Product Image Rules

Uploaded product PNG is a protected source asset.

Do not redesign or approximate the product.

Do not change:

- model;
- color;
- silhouette;
- case/body shape;
- strap shape;
- buttons;
- crown;
- ports;
- material;
- screen proportions;
- physical details.

Allowed:

- proportional scaling;
- positioning;
- composition;
- natural contact shadow;
- ambient shadow;
- subtle separation light.

The design adapts to the product.

The product must not be structurally changed to fit the design.

---

# Allowed Visible Content

Only:

1. uploaded brand logo;
2. exact product name;
3. exact version text;
4. uploaded product PNG;
5. MD3 background geometry;
6. natural lighting and shadows.

No:

- selling points;
- specifications;
- promotions;
- extra icons;
- badges;
- certification labels;
- decorative text;
- extra logos;
- marketplace stickers.

---

# Typography

Product name:

- modern sans-serif;
- Material / Roboto / Google Sans inspired;
- Bold 700;
- preferably one line;
- maximum two lines;
- do not break words internally;
- do not shrink excessively.

Version:

- Medium 500;
- clear and readable;
- visually secondary to title;
- not faint fine print.

---

# MD3 Direction

Use Material Design 3 as visual inspiration:

- rounded geometry;
- tonal surfaces;
- large curves;
- soft gradients;
- restrained elevation;
- generous whitespace;
- adaptive color;
- clean hierarchy.

Do not make the image look like an Android app UI.

---

# Master Candidate Diversity

Five candidates must differ meaningfully in composition.

Do NOT use fixed predefined composition categories.

Explore differences in:

- product placement;
- product visual scale;
- information-zone placement;
- negative space;
- MD3 geometry;
- arcs / curves;
- tonal surfaces;
- depth;
- lighting balance;
- overall visual rhythm.

Changing only the background color does not count as a different candidate.

---

# Master Selection

After the five standalone candidates exist, wait for user selection.

Examples:

"方案3"
"选第3个"
"第三张作为母版"
"方案3，就用这个"

Once unambiguous:

MASTER_SELECTED = selected option
MASTER_APPROVED = true

The selected ORIGINAL image becomes the only production master.

---

# Variant Replacement

Image A = ORIGINAL MASTER  
Image B = uploaded new SKU PNG

This is a locked-master edit, not a new poster.

Lock:

- logo artwork;
- logo size;
- logo position;
- product-name size and position;
- version size and position;
- title/version spacing;
- product visual size;
- product visual center;
- background geometry shape;
- background geometry size;
- background geometry position;
- overall composition.

Allowed changes:

- uploaded SKU product;
- background main color;
- MD3 geometry color;
- shadow strength;
- separation lighting;
- text light/dark value only when contrast requires it.

---

# Batch SKU Mode

Batch mode MUST pause for master selection.

Flow:

1. choose master SKU;
2. generate five master candidates as separate images;
3. stop;
4. wait for user selection;
5. lock selected ORIGINAL MASTER;
6. generate remaining SKUs from that same ORIGINAL MASTER.

Do not continue to other colors before the user selects the master.

---

# QA

For every image verify:

- strict 3:4 ratio;
- target 1200 × 1600;
- uploaded logo remains visually faithful;
- logo wordmark has not been re-typeset;
- logo remains in upper-left safe area;
- logo fits within 220 × 100 px maximum bounding box;
- product remains faithful to uploaded PNG;
- product is not redesigned;
- product name is exact;
- version text is exact;
- no extra text appears;
- no extra icons or badges appear.

For master candidates also verify:

- every option is a separate standalone image;
- no collage/contact sheet/grid is used;
- no option number appears inside artwork;
- candidates are genuinely different in composition.

For variants also verify:

- logo does not move or resize;
- title/version do not move or resize;
- product center and visual scale remain consistent;
- background geometry does not move, resize, or change shape.

---

# Recommended Chat Usage

## Start a new product

Upload logo + master product PNG, then say:

使用 md3-product-main-image。
产品名称：HUAWEI WATCH FIT 5 Pro
版本文字：Глобальная версия
当前上传产品作为母版 SKU。
开始母版探索。

必须逐张生成 5 个独立的 3:4 母版候选。
不要拼版。
如果一次无法输出 5 张独立图片，先只生成方案 1。

## Continue options

继续生成方案 2。
保持全部规范。
只生成一张独立 3:4 图片，不得拼版。

Repeat for 3, 4, and 5.

## Select master

方案 3 作为正式 ORIGINAL MASTER，锁定。

## Generate a variant

Upload ORIGINAL MASTER + new SKU PNG, then say:

使用已锁定的 ORIGINAL MASTER。
Image A 是正式母版。
Image B 是当前 SKU PNG。
进入 REPLACE_VARIANT。
严格锁定版式，只替换产品并适配主题色。

## Batch SKU

Upload logo + all SKU PNGs, then say:

使用 BUILD_SKU_SET。
黑色作为母版 SKU。
先逐张生成 5 个独立母版候选。
不要拼版。
生成完候选后等待我选择，不要提前生成其他颜色。
