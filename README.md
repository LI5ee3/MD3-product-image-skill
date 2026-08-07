# md3-product-main-image

A GPT-image skill for generating locked MD3-style e-commerce product main
images for Ozon. It uses a master-template-first workflow so every color SKU of
the same product shares one exact layout.

> Scope: GPT-image only. This skill does not use Photoshop, PSD files, JSX
> scripts, websites, or deployment pipelines.

## Modes

| Mode | What it does |
| --- | --- |
| CREATE_MASTER | Creates the first 1200 × 1600 px master for one product |
| REPLACE_VARIANT | Swaps the product inside an already-confirmed master for one new color SKU |
| BUILD_SKU_SET | Generates one master, then builds every remaining SKU from that locked master, one at a time |

## How to use

Place the folder in `~/.codex/skills/md3-product-main-image/` (or install the
zip), then ask in natural language:

- Create a master:
  "Create an MD3 master main image for this product, black SKU, 1200×1600."
- Replace one variant:
  "This is the confirmed master; generate the blue SKU from this PNG."
- Build a SKU set:
  "Build main images for black, blue, and gray SKUs of this product."

## Files

```text
md3-product-main-image/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── prompts/
│   ├── create-master.md
│   ├── replace-variant.md
│   └── build-sku-set.md
├── references/
│   └── design-rules.md
└── README.md
```

## Locked-master rule

Once you confirm a master, the skill never redesigns it. Variants may only
change the product image, background theme colors, shadow strength, and text
contrast — nothing else.

## 中文快速说明

- 仅使用 GPT-image 生成，不涉及 Photoshop / PSD / 网站流程。
- 每个产品独立创建一张 MD3 母版（1200 × 1600 px，适合 Ozon）。
- 同款不同颜色 SKU 必须锁定母版版式，只允许更换产品 PNG、背景主色、
  背景几何元素颜色、阴影强弱和必要的文字明暗。
- 批量模式先出 1 张母版，再逐个替换每个 SKU，禁止并行独立设计。
- 母版确认后，绝不再回到 CREATE_MASTER。

