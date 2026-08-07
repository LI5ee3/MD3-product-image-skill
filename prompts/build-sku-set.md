# Build SKU Set Prompt

Use for **MODE C — BUILD_SKU_SET**. Fill every placeholder, attach the brand
logo and base product PNG, then send to GPT-image. Attach additional SKU PNGs
one at a time per step below; never generate variants independently.

```text
Build a complete product main image set for {{PRODUCT_NAME}}
(version: {{VERSION_TEXT}}) in MD3 style for Ozon.

SKU list:
{{SKU_LIST}}

Mandatory workflow:
1. First generate ONE master image using the attached brand logo and the base
   product PNG ({{BASE_SKU}}, color {{BASE_COLOR}}), following the master
   rules: 1200 x 1600 px, only logo, product name, version text, product,
   MD3 background geometric elements, and natural light/shadow. No other text
   or graphics.
2. QA the master: confirm the layout is clean, text is correct, and the product
   is clearly separated from the background.
3. Then, one SKU at a time, generate each variant by replacing the product in
   that same locked master with the SKU's product PNG. Only the product PNG,
   background main color, background geometry colors, shadow strength, and
   necessary text contrast may change.
4. Never design any variant independently or in parallel. Every variant must
   derive from the same locked master.
5. After each variant, verify: layout lock is preserved, no extra text or
   graphics appeared, and the product is clearly separated from the background.

Output: the master plus one 1200 x 1600 px image per SKU, each labeled with its
SKU name or color.
```

