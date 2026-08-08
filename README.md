# MD3 产品主图 Skill v5.0

这是一次完全重构版本。

v5.0 不再通过不断增加“禁止某种颜色”“避免某种风格”的规则修补生成偏差。

新的设计原则是：

> **限制质量与功能，不限制具体色相，不限制固定视觉气质。**

---

# v5.0 解决的问题

之前版本中，较多的：

- 明亮
- 轻盈
- 活泼
- 年轻
- 某些推荐背景色
- 某些禁止色

容易成为模型的强视觉锚点。

结果可能出现：

- 五个候选颜色雷同
- 不同产品持续使用相似色系
- 候选之间像前一张的小改版
- MD3 被理解成固定圆弧 + Tonal Surface 模板

v5.0 删除这种做法。

---

# v5.0 核心逻辑

Skill 只控制：

- Logo 和产品素材真实性
- 3:4 画布
- 信息区位置和层级
- 电商缩略图识别度
- MD3 设计语言
- 候选独立性
- ORIGINAL MASTER 锁定
- SKU 结构一致性

不预设：

- 固定背景色
- 固定色相
- 固定冷暖
- 固定明度风格
- 固定视觉情绪
- 固定 MD3 元素组合
- 固定构图模板

---

# 五个母版候选

5 个候选必须是 5 张独立图片。

候选之间不是连续迭代。

每一张都从相同原始素材重新开始独立设计。

即：

Logo + Product + Text
→ Independent Design 1

Logo + Product + Text
→ Independent Design 2

Logo + Product + Text
→ Independent Design 3

而不是：

方案 1
→ 修改
→ 方案 2
→ 再修改
→ 方案 3

候选差异主要来自构图与空间组织。

颜色不设强制差异配额。

---

# 自适应配色

不使用：

“黑色产品应该配什么背景”
“白色产品应该配什么背景”
“蓝色产品应该配什么背景”

这类固定颜色映射。

每个产品和每个候选根据：

- 明度
- 饱和度
- 材质
- 视觉重量
- 产品与背景分离
- 当前构图
- MD3 Tonal Balance
- 缩略图表现

独立判断配色。

具体色相自由。

---

# MD3

MD3 是设计语言参考，不是固定模板。

不要求每张图都必须有：

- 圆弧
- 圆形
- 渐变
- 底座
- Tonal Surface
- 某一种固定结构

只要求设计整体符合 MD3 的层级、空间、Tonal 和几何逻辑。

---

# SKU 变体

正式母版选定后：

锁定结构：

- Logo
- 信息区
- 产品展示区域
- 产品视觉尺寸逻辑
- 产品视觉中心
- 背景几何形状 / 大小 / 位置
- 整体构图

允许当前 SKU 自适应：

- 背景主色
- 几何填充色
- Tonal Surface 配色
- 阴影
- 必要分离光
- 必要的文字明暗

每个 SKU 独立重新判断配色。

不得使用前一个 SKU 作为下一个 SKU 的生成来源。

---

# Skill 使用提示词（简洁版）

## 1. 新产品生成母版

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
```

如果只能逐张生成，后续直接发送：

```text
继续下一个母版候选。
```

---

## 2. 选择正式母版

```text
方案 3 作为 ORIGINAL MASTER。
```

将数字替换为实际选择的方案。

---

## 3. 生成其他 SKU

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

## 4. 批量 SKU

上传：

- 品牌 Logo
- 多个同款 SKU 产品 PNG

发送：

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

普通聊天中没有加载 Skill 时，可以直接使用：

- `prompts/create-master.md`
- `prompts/replace-variant.md`

如果已经加载 Skill，建议使用上面的简洁调用方式，不需要重复 Skill 内的完整规则。

---

# 文件结构

- `SKILL.md`
- `README.md`
- `prompts/create-master.md`
- `prompts/select-master.md`
- `prompts/replace-variant.md`
- `prompts/build-sku-set.md`
- `references/design-rules.md`
