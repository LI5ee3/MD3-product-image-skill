# MD3 产品主图 Skill v5.2

v5.2 的核心不是增加更多禁止项，而是重新划分规则职责：

> **硬约束要具体，创意规则要抽象。**

---

# 为什么这样改

设计类 Skill 如果不断加入：

- 不要某种颜色
- 不要某种背景
- 不要某种展台
- 不要某种场景
- 必须某种气质

这些词本身都会成为视觉锚点。

即使前面有“不要”，模型仍然会持续关注这些元素，最后可能从一种模板化走向另一种模板化。

因此 v5.2 删除针对具体创意形式的防御性条款，不再逐项列举“不要什么”。

---

# v5.2 的两类规则

## A. 强约束

保留且写清楚：

- 画布 3:4
- 1200 × 1600 px
- Logo 原子化保护
- Logo 左上安全区
- Logo 最大尺寸
- 产品 PNG 不重绘、不改色
- 产品名称与版本文字
- 信息区位于上半部分
- 信息区对齐与间距
- 禁止额外文字
- ORIGINAL MASTER 锁定
- SKU 直接从 ORIGINAL MASTER 生成
- 单回合只生成 1 张母版候选

这些属于“必须正确”的内容。

## B. 创意空间

不再规定：

- 背景色
- 冷暖
- 明度风格
- 情绪
- 构图类型
- 场景类型
- 是否有承托结构
- 用什么几何元素
- 用什么光影方式

这些由模型根据当前产品自行判断。

---

# MD3 的定义

MD3 只作为设计语言参考。

不要求固定出现：

- 某种圆弧
- 某种 Tonal Surface
- 某种底座
- 某种几何组合

模型根据当前产品和构图，自由决定空间、几何、Tonal 和层级组织。

只要求整体视觉逻辑符合 MD3，而不是把 MD3 变成固定组件模板。

---

# 缩略图可读性

原来的“电商商品卡片”类描述已降级为纯功能要求。

只检查：

- 产品是否容易识别
- 产品与背景是否分离
- 标题是否基本可读
- 信息层级是否清楚

不再告诉模型：

- 应该使用什么构图
- 应该使用什么场景
- 应该采用什么展示结构

---

# 母版候选

网页聊天模式下：

**单回合只生成 1 张候选。**

如果需要 5 张：

- 方案 1 → 独立生成
- 方案 2 → 独立生成
- 方案 3 → 独立生成
- 方案 4 → 独立生成
- 方案 5 → 独立生成

每个候选都从原始素材重新开始，不把上一张作为小改版基础。

---

# Skill 使用提示词（简洁版）

## 1. 生成第一张母版候选

上传：

- 品牌 Logo
- 母版 SKU 产品 PNG

发送：

```text
使用 md3-product-main-image。

产品名称：{{产品名称}}
版本文字：{{版本文字}}

上传的 Logo 为品牌 Logo。
上传的产品 PNG 作为母版 SKU。

进入 CREATE_MASTER_OPTIONS。
当前回合只生成 1 张独立母版候选图。
```

## 2. 继续下一张

```text
继续生成下一张独立母版候选图。
从原始输入重新独立设计，不把上一张作为修改基础。
```

## 3. 选择母版

```text
方案 3 作为 ORIGINAL MASTER。
```

## 4. 生成 SKU 变体

上传：

- ORIGINAL MASTER
- 当前 SKU 产品 PNG

发送：

```text
使用 md3-product-main-image。

Image A：ORIGINAL MASTER
Image B：当前 SKU 产品 PNG

进入 REPLACE_VARIANT。
```

## 5. 批量 SKU

```text
使用 md3-product-main-image。

产品名称：{{产品名称}}
版本文字：{{版本文字}}

{{指定 SKU}}作为母版 SKU。
其他上传图片为同款其他 SKU。

进入 BUILD_SKU_SET。
```

---

# 长版 Prompt

未加载 Skill 时，可直接使用：

- `prompts/create-master.md`
- `prompts/replace-variant.md`

已加载 Skill 时，建议使用上述简洁调用方式。

---

# 文件结构

- `SKILL.md`
- `README.md`
- `prompts/create-master.md`
- `prompts/select-master.md`
- `prompts/replace-variant.md`
- `prompts/build-sku-set.md`
- `references/design-rules.md`
