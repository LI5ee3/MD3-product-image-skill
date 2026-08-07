# Replace Variant Prompt

Use for **MODE B — REPLACE_VARIANT**. Fill every placeholder, attach the locked
master image first and the new product PNG second, then send to GPT-image.

```text
You are replacing the product in a locked master image. Do not redesign.

Image A (first attached image) is the approved master.
Image B (second attached image) is the product PNG for SKU
"{{SKU_NAME}}" (color: {{SKU_COLOR}}).

Product name: "{{PRODUCT_NAME}}".
Version text: "{{VERSION_TEXT}}".

Preserve exactly:
- Logo size and position.
- Product name size, position, and Bold 700 styling.
- Version text size, position, and Medium 500 styling.
- Spacing and alignment between product name and version text.
- Background geometric shape types, sizes, and positions.
- Product showcase area position and size.
- Overall MD3 direction and composition.

Replace:
- Image B must occupy the same showcase area as the master product, at the
  same visual size, center position, and placement logic.

Allow subtle changes only:
- Background main color tuned to {{SKU_COLOR}}.
- Background geometry colors.
- Shadow strength.
- Text lightness or darkness only when needed for contrast.

Forbidden:
- Changing any layout, size, position, shape, or typography relationship.
- Adding text, selling points, promo labels, badges, prices, or icons.
- Redesigning the composition or the MD3 style.

Goal: the result must look like the same master with only the product PNG and
theme colors swapped.

Output: one 1200 x 1600 px image.
```

