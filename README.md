# MD3 Product Main Image Skill

GPT-image-only workflow for creating product main images.

No Photoshop.
No PSD.
No website integration.
No external compositing.

## Modes

### CREATE_MASTER

Use for the first approved image of a new product.

Example:

为 Redmi Watch 6 创建 MD3 产品主图母版。
产品名称：Redmi Watch 6
版本：Глобальная версия
黑色作为母版。

---

### REPLACE_VARIANT

Use after a master is approved.

Example:

Image A 是确认好的母版。
Image B 是蓝色版本 PNG。

按锁定母版模式生成蓝色 SKU。

---

### BUILD_SKU_SET

Use when multiple colors are supplied together.

Example:

为 Redmi Watch 6 生成黑、蓝、白三色主图。
黑色做母版。
使用批量 SKU 模式。

The Skill must:

1. generate black master;
2. use that master for blue;
3. use that same master for white.

It must not independently design three posters.

---

## Principle

Different products:

may have different layouts.

Same product:

all color SKUs use one locked master.

All products:

use MD3 design principles.
