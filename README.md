# MD3 产品主图 Skill v6.2

v6.2 是一次**完整重构版本**，不是在 v6.1 上继续追加规则。

今后更新本 Skill 时，也应重新整理完整规则，而不是不断叠加补丁。

这样可以减少：
- 规则重复
- 新旧规则冲突
- 禁止项累积
- 创意空间被逐步锁死

## 核心方向

只使用 **Classic Material Design 3**。

核心视觉原则：

> **Graphic-first, depth-second**

## 最大变化：硬约束执行闭环

所有生成都必须经过：

```text
PREFLIGHT
   ↓
GENERATE
   ↓
VALIDATE
```

### PREFLIGHT
生成前确认：
- 只输出 1 张
- portrait 3:4
- 目标 1200 × 1600 px
- 不允许其他比例替代
- 不允许先生成其他比例再裁切
- Logo、产品 PNG、产品名称、版本文字均已确认

如果无法保证严格 3:4：
- 不生成无效候选

### VALIDATE
生成后检查：
- 是否只有 1 张
- 是否严格 3:4
- 是否没有通过裁切得到 3:4
- Logo 是否正确
- 产品是否正确
- 文字是否正确
- 是否有额外内容

不合格输出不计为有效候选。

## 母版候选

每回合只生成 1 张。

需要 5 张时逐张生成。

每张都从原始输入重新开始，不把上一张作为小改版基础。

## SKU

所有 SKU 直接从：

```text
ORIGINAL MASTER + 当前 SKU PNG
```

生成。

禁止：

```text
SKU1 → SKU2 → SKU3
```

## SKU 背景区分

同一产品不同颜色 SKU：
- 不重复相同背景主色
- 不使用高度接近的 hue family
- 不使用几乎一样的 tonal palette
- 不能只改一点亮度

缩略图并排时应能明显区分。

同时保持：
- Classic M3 tonal harmony
- 产品与背景分离
- 不使用固定颜色映射
- 不为了区别使用随意冲突色

---

# 简洁使用提示词

## 第一张母版候选

```text
使用 md3-product-main-image。

产品名称：{{产品名称}}
版本文字：{{版本文字}}

上传的 Logo 为品牌 Logo。
上传的产品 PNG 作为母版 SKU。

进入 CREATE_MASTER_OPTIONS。
当前回合只生成 1 张独立母版候选图。
```

## 下一张候选

```text
继续生成下一张独立母版候选图。

从原始输入重新独立设计，
不要把上一张作为修改基础。
```

## 选择母版

```text
方案 3 作为 ORIGINAL MASTER。
```

## SKU 替换

```text
使用 md3-product-main-image。

Image A：ORIGINAL MASTER
Image B：当前 SKU 产品 PNG

进入 REPLACE_VARIANT。
```

## 批量 SKU

```text
使用 md3-product-main-image。

产品名称：{{产品名称}}
版本文字：{{版本文字}}

{{指定 SKU}}作为母版 SKU。
其他上传图片为同款其他 SKU。

进入 BUILD_SKU_SET。
```

---

# 文件结构

```text
md3-product-main-image-v6.2/
├── SKILL.md
├── README.md
├── prompts/
│   ├── create-master.md
│   ├── continue-master.md
│   ├── select-master.md
│   ├── replace-variant.md
│   └── build-sku-set.md
└── references/
    ├── classic-m3-principles.md
    └── execution-contract.md
```

## 版本维护原则

后续每次更新：
- 重新整合完整规则
- 删除已被新规则替代的旧表达
- 避免重复限制
- 区分硬约束与创意规则
- 防止新增规则形成新的视觉锚点
