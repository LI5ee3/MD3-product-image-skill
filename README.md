# MD3 产品主图 Skill v6.1

v6.1 是一次重新整理后的完整版本。

本版本只使用：

> **Classic Material Design 3**

作为唯一视觉设计语言。

---

# 一、v6.1 的设计目标

之前的版本在两个方向之间出现过摆动：

1. 对风格描述过多，导致候选颜色和构图趋同
2. 对创意限制过少，导致画面偏向高写实棚拍 / 建筑空间

v6.1 不再通过增加大量“禁止项”解决问题。

新的方式是：

> **使用 Classic M3 官方基础体系作为正向设计依据，同时保持具体构图和配色自由。**

---

# 二、Classic M3 在本 Skill 中的含义

重点使用五个基础概念：

- Color
- Shape
- Surface
- Elevation
- Typography

不是把 Material 3 做成 Android UI。

也不是要求每张图都出现固定的：

- 圆形
- 圆弧
- 底座
- 某种浅蓝背景
- 某种固定 Surface 组合

---

# 三、静态产品视觉适配

v6.1 的核心适配原则：

> **Graphic-first, depth-second**

即：

先建立：

- Surface
- Shape
- tonal relationships
- 信息层级

再加入：

- 适度 Elevation
- 柔和阴影
- 轻量空间深度

产品本身保持真实。

最终画面应首先呈现为：

> **经过设计的 Classic M3 图形构成**

而不是以真实摄影棚或建筑空间为主要设计语言。

---

# 四、强约束与创意自由

## 强约束

必须严格执行：

- 3:4
- 目标 1200 × 1600 px
- Logo 原子化保护
- Logo 左上安全区
- 产品 PNG 不重绘、不改色
- 产品名称与版本文字
- 信息区位于上半部分
- 禁止额外文字
- ORIGINAL MASTER 锁定
- SKU 不链式派生
- 单回合只生成 1 张候选

## 创意自由

不预设：

- 固定背景色
- 固定冷暖
- 固定构图
- 固定 Shape
- 固定 Surface 数量
- 固定场景
- 固定视觉情绪

具体设计由当前产品独立决定。

---

# 五、母版候选

网页聊天模式下：

**单回合只生成 1 张候选图。**

需要更多方案时逐张继续。

每一张都：

- 从原始输入重新开始
- 不以上一张作为小改版
- 不默认继承上一张配色和构图

---

# 六、Skill 使用提示词（简洁版）

## 1. 生成第一张母版候选

上传：

- 品牌 Logo
- 当前产品 PNG

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

---

## 2. 继续生成下一张候选

```text
继续生成下一张独立母版候选图。

从原始输入重新独立设计，
不要把上一张候选作为修改基础。
```

---

## 3. 选择 ORIGINAL MASTER

```text
方案 3 作为 ORIGINAL MASTER。
```

将数字替换为实际选择的候选。

---

## 4. 生成同款其他 SKU

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

---

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

# 七、长版 Prompt

如果没有加载 Skill，可以直接使用：

- `prompts/create-master.md`
- `prompts/replace-variant.md`

如果已经加载 Skill，建议使用上面的简洁调用提示词。

不要在调用 Prompt 中重复整个 Skill。

---

# 八、文件结构

- `SKILL.md`
- `README.md`
- `prompts/create-master.md`
- `prompts/select-master.md`
- `prompts/replace-variant.md`
- `prompts/build-sku-set.md`
- `references/classic-m3-principles.md`


---

# 九、v6.1 新增：SKU 背景区分规则

同一产品不同颜色 SKU：

- 不使用相同背景色方案
- 不使用高度接近的 tonal palette
- 缩略图中需要能够快速区分

但仍遵循 Classic M3：

- 不固定颜色映射
- 不为了区别强行使用冲突色
- 保持产品与背景协调

核心：

结构锁定，色彩自适应，但 SKU 必须具有明显视觉差异。
