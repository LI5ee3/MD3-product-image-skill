# Core scene prompt blocks

Read this file when building a scene prompt. Append every block below with its
exact words; replace only brackets and adapt the declared input role. Never
rewrite, paraphrase, or expand them.

## Style block

Append unchanged to every scene prompt:

```text
Use Google Classic Material Design 3 (MD3) as the sole visual style.

Do not use Material 3 Expressive.
```

## CORE_SCENE_BLOCK

Include in every call. Replace only brackets, adapt the declared input role, and
append the style block above:

```text
Create one portrait 3:4 e-commerce product image using the supplied inputs.

Input role: [MASTER: Image 1 is authoritative product / SKU: ORIGINAL MASTER is
composition reference and CURRENT SKU is authoritative product]. The original
Logo PNG is excluded. Do not render or approximate information-group Logo or text.

Future information is excluded from this call. Protect only these normalized
canvas zones; never infer or render their future content:
- invisible stepped information clear zones:
  [INFORMATION_CLEAR_ZONES as a resolved labeled x/y/w/h list]

Together these zones form one compact connected stepped area on the same
uninterrupted base field, not their outer bounding rectangle or a scene object.
Do not show their bounds or place any panel, bar, card, plaque, backing, edge,
shadow, platform, or separate surface inside them. Do not reserve unused space
outside the zones merely because it falls inside their overall outer bounds.

Generate the complete product scene now. Product, environment, platform,
lighting, shadows, reflections, ambient response, perspective, scale, and
spatial relationships must form one coherent image. Do not generate a
background-only image or leave product placement for later compositing.

Create a graphic-first Google Classic MD3 product showcase with large overlapping 2.5D rounded panels, 2.5D organic geometric fields, restrained physical depth, matte surfaces, soft elevation, and a low 2.5D product platform. Keep it spacious and layered, not a realistic room, architectural interior, furniture scene, or physical exhibition environment.

Make every major background rounded panel and organic geometric field visibly
shallow 2.5D scene geometry, never a flat filled region. Show visible shallow
edge thickness plus overlap, occlusion, or a short soft elevation shadow that
follows the primary light direction. Keep the depth restrained and graphic;
do not turn these fields into walls, architecture, or a deep 3D set.

Analyze the current product's actual colors, brightness, saturation, material,
finish, visual weight, and local accent colors; derive the palette from the
current product without prescribing colors. Preserve authentic product colors. Do not let the major panels and geometric
fields collapse into one repeatedly used near-identical hue family. At thumbnail
size, use a product-informed dominant palette family plus one clearly
distinguishable controlled contrast hue family. Use the contrast family in one
major field and, when useful, no more than one smaller supporting field. Keep its
perceived saturation or chroma consistent with the scene's chromatic palette;
for a neutral product, keep it restrained. Avoid a sudden vivid accent, and never
let it become a focal point or disturb the mandatory hierarchy. Keep it outside
the protected information zones.

Adjust platform and adjacent-field hue and lightness so the entire silhouette,
lower body, and contact area remain clear at normal and thumbnail size. When
hues are similar, create a clear light-dark difference. Do not rely on
saturation, partial contrast, outlines, halos, glows, or product backing. The
platform top must not merge with the product.

Render exactly one faithful product. Preserve identity, geometry, proportions,
construction, materials, controls, display content, colors, and details. Do not
redesign, deform, simplify, recolor, replace, duplicate, or invent components.
Match lighting, perspective, reflections, contact shadows, and ambient occlusion;
reject floating or pasted-on appearance.

Keep the declared information clear zones as compact connected upper-left
negative space on one continuous base field. Do not let the product, a
background boundary, or any visible information backing enter a protected
content zone or connector. A background boundary may occupy unused space outside
the zones, including unused space inside their overall outer bounds, when it
does not visually fragment or reduce the legibility of the information group.

Keep product first in focus, future title second, Logo third, and version fourth.
Use clean high-key studio lighting from a large upper-front soft source, gentle
fill, restrained separation light, short diffused contact shadows, and
controlled reflections.

Outside authentic product markings, generate no text, Logo, letters, numbers,
icons, labels, badges, prices, specifications, slogans, promotions, or
watermarks. Avoid information cards, extra backing shapes, multiple products,
duplicate-like reflections, rooms, furniture, shelves, props, boxes, detailed
scenery, busy patterns, neon, glassmorphism, excessive gradients, deep
perspective, product deformation, extra text, and marketplace graphics.
```
