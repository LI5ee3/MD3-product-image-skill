---
name: md3-product-main-image
version: 6.0
description: >
  GPT-image-only workflow for product main images using Classic Material Design 3
  as the sole visual design language. The skill strictly protects source assets,
  canvas, information layout, and master/SKU consistency while keeping composition
  and palette adaptive within Classic M3 foundations.
---

# MD3 Product Main Image Skill v6.1

## 1. 唯一设计语言

本 Skill 只使用 **Classic Material Design 3** 作为视觉设计依据。

不把 Material 3 当成固定模板，也不把它理解成 Android UI 组件集合。

本任务只提取与静态产品视觉相关的基础原则：

- Color / tonal relationships
- Shape
- Surface
- Elevation
- Typography / hierarchy

详细解释见：

`references/classic-m3-principles.md`

---

## 2. 核心原则

### 强约束必须明确

严格控制：

- 源素材真实性
- 画布比例
- Logo
- 产品 PNG
- 产品名称
- 版本文字
- 信息区
- ORIGINAL MASTER
- SKU 替换关系
- 单回合输出数量

### 创意部分保持开放

不预设：

- 固定背景色
- 固定冷暖
- 固定色相家族
- 固定构图模板
- 固定产品展示结构
- 固定场景
- 固定情绪
- 固定几何组合

Classic M3 负责提供视觉组织逻辑，
而不是提供一套重复使用的海报模板。

---

# 3. 工作状态

1. CREATE_MASTER_OPTIONS
2. WAIT_FOR_MASTER_SELECTION
3. REPLACE_VARIANT
4. BUILD_SKU_SET

---

# 4. CREATE_MASTER_OPTIONS

用于创建新的母版候选。

## 单回合输出

每个回合只生成 **1 张独立母版候选图**。

禁止：

- 拼版
- 五宫格
- Contact Sheet
- Collage
- Grid
- Multi-panel
- 一张图同时展示多个候选
- 图片内部添加候选编号

需要更多候选时，由用户继续要求生成下一张。

## 候选必须独立设计

每个候选都从同一组原始输入重新开始：

BRAND LOGO
+ PRODUCT PNG
+ PRODUCT NAME
+ VERSION TEXT
→ NEW INDEPENDENT DESIGN

新的候选不得以上一张候选作为设计起点。

不要默认继承上一张候选的：

- 构图
- 配色
- 产品位置
- 产品视觉尺寸
- Surface 组织
- 几何关系
- 空间层级
- 光影
- 视觉节奏

每个候选重新根据当前产品进行完整设计判断。

如果独立判断后自然出现相似点，可以接受。

不要为了制造差异而强行改变颜色或构图。

生成当前候选后停止，等待用户继续或选择母版。

---

# 5. WAIT_FOR_MASTER_SELECTION

仅在用户明确选择后锁定母版。

例如：

- 方案3
- 第三张作为母版
- 选第3个
- 方案3作为 ORIGINAL MASTER

选中的原始候选图成为唯一：

**ORIGINAL MASTER**

禁止：

- 混合其他候选
- 重新生成“类似母版”
- 使用未选中的候选派生 SKU

---

# 6. REPLACE_VARIANT

输入：

- Image A = ORIGINAL MASTER
- Image B = 当前同款 SKU 产品 PNG

这是锁定母版后的产品替换。

不是重新设计主图。

每个 SKU 必须直接从：

ORIGINAL MASTER + CURRENT SKU

生成。

正确：

- ORIGINAL MASTER + SKU 2
- ORIGINAL MASTER + SKU 3
- ORIGINAL MASTER + SKU 4

错误：

- MASTER → SKU 2 → SKU 3 → SKU 4

禁止使用前一个 SKU 变体作为下一个 SKU 的来源。

---

# 7. BUILD_SKU_SET

用于同一产品多个 SKU。

流程：

1. 指定母版 SKU
2. 使用母版 SKU 生成第 1 张独立候选
3. 停止
4. 用户需要时继续逐张生成其他候选
5. 用户选择 ORIGINAL MASTER
6. 锁定 ORIGINAL MASTER
7. 其他 SKU 全部直接从 ORIGINAL MASTER 生成

正式母版未选定前，不得提前生成其他 SKU。

---

# 8. 画布

所有输出必须：

- 比例：3:4
- 目标尺寸：1200 × 1600 px

不得先生成其他比例再裁切。

---

# 9. Logo 保护

上传 Logo 是一个不可拆分的完整图形。

Logo 内所有内容均属于 Logo 本体，包括：

- Symbol
- Emblem
- Wordmark
- 品牌文字
- 字形
- 字距
- 字重
- 内部比例
- 内部对齐
- 颜色
- 透明区域
- 边缘细节

Logo 内嵌文字不是可编辑文字。

禁止：

- OCR 后重新打字
- 重新生成 Wordmark
- 修改字形
- 修改字距
- 修改字重
- 拆分 Logo
- 重建 Logo
- 使用相似 Logo 替代

只允许：

- 整体等比例缩放
- 整体定位

---

# 10. Logo 位置与尺寸

Logo 位于左上安全区。

1200 × 1600 px：

- 左边距 ≥ 60 px
- 上边距 ≥ 80 px

最大包围框：

- 宽度 ≤ 220 px
- 高度 ≤ 100 px

保持原始宽高比。

候选中 Logo 视觉尺寸保持一致。

ORIGINAL MASTER 选定后：

- Logo 位置锁定
- Logo 宽度锁定
- Logo 高度锁定

---

# 11. 信息区

Logo、产品名称、版本文字组成稳定信息区。

必须：

- 产品名称位于 Logo 下方
- 产品名称与版本文字位于主图上半部分
- 标题优先与 Logo 形成统一视觉左轴
- 版本文字与标题左对齐
- Logo → 标题保持合理间距
- 标题 → 版本保持清晰层级间距
- 信息区不得侵入产品核心展示区

长标题：

- 优先一行
- 必要时最多两行
- 不得从单词中间断开
- 可适度缩小字号
- 信息区仍须位于上半部分

ORIGINAL MASTER 选定后锁定：

- Logo / 标题左轴关系
- 标题位置
- 版本位置
- Logo → 标题间距
- 标题 → 版本间距
- 整个信息区结构

---

# 12. 产品 PNG 保护

上传产品 PNG 是产品外观的唯一权威来源。

禁止：

- 重绘产品
- 用相似型号替代
- 修改产品颜色
- 修改轮廓
- 修改结构
- 修改材质
- 修改屏幕比例
- 修改按钮 / 表冠 / 接口 / 孔位
- 添加不存在的硬件
- 删除真实细节

只允许：

- 等比例缩放
- 定位
- 构图摆放
- 与画面一致的自然阴影
- 必要的轻微分离光

---

# 13. 画面允许内容

只允许：

1. 上传品牌 Logo
2. 精确产品名称
3. 精确版本文字
4. 上传产品 PNG
5. Classic M3 视觉设计元素
6. 服务于层级关系的自然光影

产品本身真实存在的文字和屏幕内容可保留。

禁止新增：

- 功能卖点
- 参数
- 促销信息
- 折扣标签
- 认证
- 额外 Logo
- 额外图标
- 徽章
- 装饰性英文
- 平台贴纸
- 虚构 UI

---

# 14. Typography

产品名称：

- 现代中性无衬线
- Google Sans / Roboto / Material-like
- Bold 700
- 清晰、主要层级
- 优先一行
- 最多两行

版本文字：

- Medium 500
- 清晰可读
- 作为次级文字层级
- 不得过小或像脚注

---

# 15. Classic Material 3 视觉逻辑

设计应以 Classic M3 的基础体系组织静态产品视觉。

## Color

颜色首先承担：

- Surface 区分
- 层级
- 视觉组织
- 产品分离

使用协调的 tonal relationships。

不设置固定色表。

不设置“产品颜色 → 背景颜色”映射。

具体 hue 根据当前产品独立决定。

## Shape

Shape 用于：

- 建立整体视觉结构
- 引导注意力
- 组织 Surface
- 建立产品与背景关系

不规定必须使用某一种形状。

不固定圆形、圆角矩形、曲线或其他具体组合。

## Surface

背景不是必须模拟一个真实物理空间。

优先把画面理解为多个具有层级关系的视觉 Surface。

Surface 可以承担：

- 分区
- 产品承托
- 空间组织
- 色彩关系
- 视觉节奏

## Elevation

Elevation 用于表达不同 Surface 和产品之间的层级。

可以通过：

- tonal difference
- soft shadow
- subtle depth

表达。

Elevation 是视觉层级，不要求构建写实建筑空间。

## Typography

通过字号、字重、位置和间距建立稳定信息层级。

---

# 16. Classic M3 静态产品视觉适配

本 Skill 的静态产品主图采用：

**Graphic-first, depth-second**

即：

- 首先建立清晰的图形与 Surface 构成
- 再加入适度空间深度
- 产品保持真实
- 环境设计保持简化和图形化

整体可以有立体感，但不要让写实空间本身成为主要设计语言。

色彩主要由 Surface 与 tonal relationships 建立，
而不是依赖戏剧化环境灯光制造视觉主题。

具体：

- 构图
- 配色
- Shape
- Surface
- 产品位置
- 空间关系

仍由当前产品独立决定。

---

# 17. 缩小显示可读性

只检查功能结果：

- 产品主体容易识别
- 产品与背景有清晰分离
- 产品名称保持基本可读
- 信息层级明确
- 构图完整

这条规则不规定：

- 具体构图
- 具体场景
- 具体 Shape
- 具体展示结构

---

# 18. SKU 结构锁定

REPLACE_VARIANT 时严格保留 Image A：

- Logo 样式
- Logo 大小
- Logo 位置
- 产品名称内容
- 产品名称大小
- 产品名称位置
- 版本文字内容
- 版本文字大小
- 版本文字位置
- 信息区关系
- 产品展示区域
- 产品视觉尺寸逻辑
- 产品视觉中心
- 背景 Shape
- Surface 结构
- 背景几何大小
- 背景几何位置
- 整体构图
- 基本光源方向

不得重新设计版式。

---

# 19. SKU 允许自适应

当前 SKU 可重新评估：

- 背景主色
- Surface tonal relationships
- 几何填充色
- 阴影强弱
- 必要的轻微分离光
- 必要的文字明暗

不继承前一个 SKU 的配色偏好。

核心：

**锁定结构，自适应配色。**

---


# 20. SKU Background Differentiation

同一产品的不同颜色 SKU 必须具有明显的视觉区分。

当多个 SKU 使用同一个 ORIGINAL MASTER 时：

必须重新评估当前 SKU 的背景 tonal palette。

不同 SKU 不应重复使用相同或高度接近的背景色方案。

需要避免：

- 相同背景主色
- 相同 tonal palette
- 仅调整明暗但整体视觉相同
- 仅改变阴影颜色但背景关系不变

目标：

用户在缩略图列表中即可快速区分不同颜色 SKU。

同时保持 Classic Material Design 3 原则：

- 色彩协调
- 保持 tonal relationship
- 保持产品与背景分离
- 不为了制造区别而使用冲突颜色

背景变化可以来自：

- Surface 色调变化
- Tonal palette 调整
- 几何区域色彩变化
- 环境氛围变化

禁止通过改变：

- 母版构图
- 信息区
- 产品比例
- 产品位置

来制造 SKU 差异。

SKU 输出前检查：

如果两个 SKU 缩略图并排显示，
背景是否能够快速区分。

如果无法区分，
需要重新调整当前 SKU 的背景 tonal palette。

# 21. QA

每张图检查：

- 3:4
- 目标 1200 × 1600
- Logo 与上传素材一致
- Logo 内文字未重新排版
- Logo 位于左上安全区
- 产品与上传 PNG 一致
- 产品未重绘、未改色
- 产品名称精确
- 版本文字精确
- 信息区位于上半部分
- 信息区对齐与间距合理
- 无额外文字、图标或徽章
- 产品缩小时容易识别
- 产品与背景分离清晰
- 画面由 Classic M3 的 Color / Shape / Surface / Elevation / Typography 逻辑组织
- 不是固定模板
- 没有依赖真实空间取代图形构成

母版候选额外检查：

- 当前回合只输出 1 张
- 没有拼版
- 当前候选从原始输入重新独立设计

SKU 额外检查：

- 使用 ORIGINAL MASTER
- Logo 未移动或缩放
- 信息区未重新排版
- 产品视觉中心与尺寸逻辑保持一致
- Surface / Shape 结构未改变
- 当前 SKU 配色被独立重新评估
