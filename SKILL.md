---
name: md3-product-main-image
version: 6.4
description: >
  Create product main images using Classic Material Design 3 as the sole visual language.
  The skill protects source assets, enforces a 3:4 master-image workflow, keeps information-zone
  geometry stable, and derives same-product SKU variants directly from one locked ORIGINAL MASTER.
---

# MD3 Product Main Image Skill v6.4

## 1. Design Language

Use **Classic Material Design 3 only**.

Do not use Material 3 Expressive.

For static product imagery, Classic M3 is interpreted through:

- Color
- Shape
- Surface
- Elevation
- Typography

Reference:
`references/classic-m3-principles.md`

Core visual target:

**realistic product + graphic Classic M3 environment**

Core principle:

**Graphic-first, depth-second.**

---

## 2. Execution Model

Every generation follows:

**PREFLIGHT → GENERATE → VALIDATE**

Hard-constraint failures are not repaired locally.

If a hard constraint fails:

**invalidate the whole result → regenerate from original inputs**

---

## 3. Workflow States

1. `CREATE_MASTER_OPTIONS`
2. `WAIT_FOR_MASTER_SELECTION`
3. `REPLACE_VARIANT`
4. `BUILD_SKU_SET`

---

## 4. PREFLIGHT

Before generation, verify the applicable hard constraints.

### Canvas
- exactly 1 image in the current round
- portrait
- exact 3:4 aspect ratio
- target size 1200 × 1600 px
- no substitute ratio
- no crop-to-3:4 workflow

If exact 1200 × 1600 is unavailable but exact 3:4 is guaranteed, proportional resizing without cropping is allowed.

If exact 3:4 cannot be guaranteed, do not generate.

### Required inputs
- source brand Logo is available
- source product PNG is available
- exact product name is known
- exact version text is known

### Master-candidate mode
- one standalone candidate only
- no collage, grid, contact sheet, or multi-panel
- no candidate number inside the artwork

### Variant mode
- Image A is the approved ORIGINAL MASTER
- Image B is the current SKU source PNG

---

## 5. CREATE_MASTER_OPTIONS

Generate one standalone master candidate per round.

Each candidate starts again from:

`BRAND LOGO + PRODUCT PNG + PRODUCT NAME + VERSION TEXT`

Do not use the previous candidate as a redesign base.

Do not automatically inherit the previous candidate's:

- composition
- palette
- product position
- product scale
- Shape arrangement
- Surface arrangement
- spatial hierarchy
- lighting
- visual rhythm

Natural similarity is acceptable if independently judged appropriate.

After one valid candidate is generated, stop and wait for the user to continue or select a master.

---

## 6. WAIT_FOR_MASTER_SELECTION

Only lock a master after explicit user selection.

The selected original candidate becomes the sole:

**ORIGINAL MASTER**

Do not:

- blend rejected candidates
- regenerate a substitute master
- derive SKUs from an unselected candidate

---

## 7. REPLACE_VARIANT

Inputs:

- Image A = ORIGINAL MASTER
- Image B = current SKU source PNG

This is a locked-master product replacement, not a new poster design.

Every SKU derives directly from:

`ORIGINAL MASTER + CURRENT SKU`

Correct:

- ORIGINAL MASTER + SKU 2
- ORIGINAL MASTER + SKU 3
- ORIGINAL MASTER + SKU 4

Incorrect:

- MASTER → SKU 2 → SKU 3 → SKU 4

Never use a generated SKU variant as the source for another SKU.

---

## 8. BUILD_SKU_SET

1. choose the master SKU
2. generate master candidates one at a time
3. user selects ORIGINAL MASTER
4. lock ORIGINAL MASTER
5. generate every remaining SKU directly from ORIGINAL MASTER

Do not generate remaining SKUs before master approval.

---

## 9. Brand Logo Protection

Treat the uploaded Logo as one indivisible protected graphic.

Everything inside the source Logo belongs to the asset, including:

- symbol
- emblem
- wordmark
- brand text
- letterforms
- spacing
- weight
- internal proportions
- alignment
- colors
- transparency
- edge detail

Embedded Logo text is not editable text.

Only proportional scaling and positioning are allowed.

Do not recreate, re-typeset, split, rebuild, recolor, or substitute the Logo.

---

## 10. Logo Placement and Scale

On a 1200 × 1600 canvas:

- visible Logo left edge ≥ 60 px
- visible Logo top edge ≥ 80 px
- entire visible Logo remains inside the canvas

Maximum visible Logo bounds:

- width ≤ 220 px
- height ≤ 100 px

Use the **visible artwork bounds**, not the transparent PNG canvas bounds, for alignment.

Preserve source aspect ratio.

Across master candidates, keep Logo visual scale consistent.

After ORIGINAL MASTER approval, Logo position and scale are locked.

---

## 11. Atomic Information Zone

Treat:

**Logo + Product Name + Version Text**

as one layout system.

Use one shared visual left axis:

**INFO_X**

Preferred alignment:

- visible Logo left edge = INFO_X
- product-name left edge = INFO_X
- version-text left edge = INFO_X

Required structure:

- product name below Logo
- product name and version remain in the upper half
- Logo → product name spacing is stable
- product name → version spacing is stable
- information zone does not invade the core product display area

Long product names:

- prefer one line
- maximum two lines
- do not split words internally
- moderate size reduction is allowed
- information zone remains in the upper half

After ORIGINAL MASTER approval, lock the entire information-zone geometry.

---

## 12. No Local Repair of Hard Constraints

Logo, product, information-zone geometry, and canvas ratio must be correct in the full-image generation.

Do not perform local repainting or local regeneration to fix:

- Logo size or position
- Logo artwork
- title alignment
- version alignment
- product fidelity
- canvas ratio

If any of these fail, invalidate the whole result and regenerate from original inputs.

This prevents:

- rectangular background color mismatch around Logo repairs
- broken background continuity
- Logo/title alignment drift
- product patch artifacts

---

## 13. Product Asset Protection

The uploaded product PNG is authoritative.

Do not:

- redraw
- substitute a similar model
- recolor
- alter silhouette
- alter structure
- alter material
- alter screen proportions
- alter buttons, crown, ports, or holes
- add nonexistent hardware
- remove real details

Allowed:

- proportional scaling
- positioning
- composition placement
- natural contact shadow
- restrained ambient shadow
- subtle separation light when necessary

---

## 14. Allowed Visible Content

Only:

1. source brand Logo
2. exact product name
3. exact version text
4. source product PNG
5. Classic M3 visual design elements
6. natural lighting and shadows that support hierarchy

Real text already present on the product may remain.

Do not add:

- selling points
- specifications
- promotional labels
- discounts
- certifications
- extra logos
- extra icons
- badges
- decorative copy
- marketplace stickers
- invented UI

---

## 15. Typography

Product name:

- modern neutral sans-serif
- Google Sans / Roboto / Material-like
- Bold 700
- primary text hierarchy
- prefer one line
- maximum two lines

Version text:

- Medium 500
- clearly readable
- secondary hierarchy
- not tiny or footnote-like

---

## 16. Classic M3 Static Product Visual

The product remains realistic.

The environment remains graphic, simplified, tonal, and structured.

### Color
Use tonal relationships to organize:

- Surface separation
- hierarchy
- product/background separation
- visual rhythm

No fixed color table.
No fixed product-color mapping.
Hue remains adaptive.

### Shape
Use Shape to organize:

- composition
- attention
- Surface relationships
- product/background relationships

No specific Shape is mandatory.

### Surface
Interpret Surface primarily as a:

**graphic visual layer**

Surface can establish:

- zoning
- support
- overlap
- tonal structure
- visual rhythm

It does not need to simulate literal physical materials or architecture.

### Elevation
Interpret Elevation primarily as:

**layer hierarchy**

Express it through:

- tonal difference
- overlap
- soft shadow
- restrained depth

Do not rely on realistic architectural depth as the main visual language.

### Composition order
Build in this order:

1. Surface structure
2. Shape relationships
3. tonal relationships
4. information hierarchy
5. restrained depth
6. realistic product lighting

The image should first read as a designed Classic M3 graphic composition and only secondarily as spatial.

---

## 17. Thumbnail Readability

At reduced size:

- product remains recognizable
- product/background separation remains clear
- product name remains basically readable
- hierarchy remains clear
- composition remains intact

This is a functional requirement only; it does not prescribe a specific layout or scene.

---

## 18. SKU Structure Lock

During `REPLACE_VARIANT`, preserve Image A:

- Logo artwork
- Logo scale
- Logo position
- product-name content, size, and position
- version content, size, and position
- information-zone geometry
- product display region
- product visual-scale logic
- product visual center
- Shape structure
- Surface structure
- background geometry size and position
- overall composition
- primary light direction

Do not redesign the layout.

---

## 19. SKU Adaptive Palette

For each SKU, independently reassess:

- background main color
- Surface tonal relationships
- Shape fill colors
- shadow intensity
- subtle separation light
- text light/dark value only if needed

Do not inherit the previous SKU's palette preference.

Core rule:

**Lock structure, adapt palette.**

---

## 20. SKU Background Differentiation

Different color SKUs of the same product must have clearly distinguishable background palettes.

Do not reuse:

- the same background main color
- a nearly identical hue family
- a nearly identical tonal palette
- a palette differing only by slight brightness

At thumbnail size, sibling SKUs should be obviously distinguishable.

At the same time:

- keep Classic M3 tonal harmony
- keep product/background separation
- do not use arbitrary clashing colors only to force difference
- do not change locked layout or geometry to create SKU distinction

If a new SKU is too similar to an existing one:

- preserve the locked structure
- recalculate the current SKU palette
- validate again

No fixed color mapping is used.

---

## 21. VALIDATE

Before delivery, validate:

### Hard validation
- exactly 1 image
- exact portrait 3:4
- not cropped from another ratio
- target 1200 × 1600, or exact 3:4 source eligible for proportional resize
- source Logo faithfully preserved
- source product faithfully preserved
- product name exact
- version text exact
- no extra text, icon, or badge

### Information-zone validation
- visible Logo left edge follows INFO_X
- product name follows INFO_X
- version follows INFO_X
- spacing relationships remain intact
- no local Logo patching occurred
- no rectangular background mismatch appears around the Logo

### Master-candidate validation
- one standalone candidate only
- no collage
- independently designed from original inputs

### SKU validation
- Image A is ORIGINAL MASTER
- information zone remains locked
- product center and scale logic remain consistent
- Shape / Surface structure remains locked
- current SKU palette is independently evaluated
- current SKU background is clearly distinct from sibling SKUs

If any hard validation fails:

**invalidate the result → regenerate from original inputs**

Do not locally repair the failed element.
