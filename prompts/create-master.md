# Create Master Prompt

Use for **MODE A — CREATE_MASTER**. Fill every placeholder, attach the brand
logo and product PNG, then send the prompt to GPT-image.

```text
You are creating an e-commerce product main image for Ozon in Google Material
Design 3 (MD3) style.

Canvas: 1200 x 1600 px, portrait 3:4.

Allowed content only:
1. The attached brand logo.
2. Product name: "{{PRODUCT_NAME}}".
3. Version text: "{{VERSION_TEXT}}".
4. The attached product PNG (color: {{PRODUCT_COLOR}}).
5. MD3-style background geometric elements: subtle tonal shapes, elevation
   surfaces, restrained geometry.
6. Natural light and shadow that give the product dimensionality.

Forbidden:
- Any other text.
- Feature selling points, parameter copy, promotional labels, badges, prices,
  ratings, or extra icons.
- Non-MD3 decorations such as heavy gradients, neon effects, or noisy patterns.

Layout:
- Logo in the top-left safe area, with a fixed size and position.
- Product name prominent, modern sans-serif, Bold 700. Prefer one line; if it
  is too long, use at most two lines. Never shrink it below readable size.
- Version text directly below the product name, Medium 500, aligned with the
  name.
- Background elements must avoid the logo, product name, and version text
  areas.
- The product is the main visual: large, centered in a stable showcase area,
  with natural light and shadow.

Color:
- Use an MD3 tonal theme matched to the product color.
- Keep clear separation between product and background; the product must not
  blend into the background.
- Dark product: graphite / deep cool gray theme.
- Light product: warm gray / cool gray / beige gray theme.
- White product: never place it on a near-white background.

Consistency — this image is the master:
- Establish fixed positions and sizes for: logo, product name, version text,
  product showcase area, and background geometry.
- This layout will be locked and reused for every future color variant of this
  product.

Output: one 1200 x 1600 px image.
```

