---
name: md3-product-main-image
version: 6.2
description: Classic Material Design 3 product-main-image workflow with hard preflight and validation.
---

# MD3 Product Main Image Skill v6.2

## 1. 唯一设计语言

只使用 **Classic Material Design 3**。

不使用 Material 3 Expressive。

Classic M3 在本任务中作为静态产品视觉设计语言，重点使用：

- Color
- Shape
- Surface
- Elevation
- Typography

详见 `references/classic-m3-principles.md`。

---

## 2. 执行总原则

所有图像任务必须执行：

**PREFLIGHT → GENERATE → VALIDATE**

硬约束不是风格建议。

如果硬约束无法保证，不得静默替换为其他值。

---

## 3. PREFLIGHT HARD CONSTRAINTS

生成前必须确认：

### 画布
- 当前回合只输出 1 张图片
- portrait
- 严格 3:4
- 目标尺寸 1200 × 1600 px
- 不允许用 1:1、4:5、2:3 或其他比例代替
- 不允许先生成其他比例再裁切成 3:4

若生成器不能原生输出 1200 × 1600，但能保证严格 3:4：
- 可在不裁切的前提下等比例缩放到 1200 × 1600
- 不得改变构图

若无法保证严格 3:4：
- 停止
- 不生成无效候选

### 必需输入
确认：
- 品牌 Logo 已上传
- 产品 PNG 已上传
- 产品名称准确
- 版本文字准确

### 输出模式
CREATE_MASTER_OPTIONS：
- 当前回合只生成 1 张独立候选
- 禁止拼版、五宫格、Contact Sheet、Collage、Grid、Multi-panel
- 图片内部不得出现方案编号

REPLACE_VARIANT：
- Image A 必须是已确认的 ORIGINAL MASTER
- Image B 必须是当前 SKU 原始产品 PNG

只有 PREFLIGHT 通过后才能进入 GENERATE。

---

## 4. 工作状态

1. CREATE_MASTER_OPTIONS
2. WAIT_FOR_MASTER_SELECTION
3. REPLACE_VARIANT
4. BUILD_SKU_SET

---

## 5. CREATE_MASTER_OPTIONS

每个回合只生成 1 张独立母版候选图。

每个新候选必须从同一组原始输入重新开始：

BRAND LOGO + PRODUCT PNG + PRODUCT NAME + VERSION TEXT
→ NEW INDEPENDENT DESIGN

不得把上一张候选作为修改基础。

不要默认继承上一张候选的：
- 构图
- 配色
- 产品位置
- 产品视觉尺寸
- Surface 结构
- Shape 结构
- 空间层级
- 光影
- 视觉节奏

如果独立判断后自然出现相似点，可以接受。

不要为了制造差异而强行换色或改构图。

生成当前候选后停止，等待用户继续或选择母版。

---

## 6. WAIT_FOR_MASTER_SELECTION

只有用户明确选择后，才锁定 ORIGINAL MASTER。

选中的原始候选图成为唯一 ORIGINAL MASTER。

禁止：
- 混合其他候选
- 重新生成“类似母版”替代
- 使用未选中的候选派生 SKU

---

## 7. REPLACE_VARIANT

输入：
- Image A = ORIGINAL MASTER
- Image B = 当前 SKU 原始产品 PNG

这是“锁定母版后的产品替换”，不是重新设计。

所有 SKU 必须直接从：

ORIGINAL MASTER + CURRENT SKU

生成。

正确：
- ORIGINAL MASTER + SKU 2
- ORIGINAL MASTER + SKU 3
- ORIGINAL MASTER + SKU 4

错误：
- MASTER → SKU 2 → SKU 3 → SKU 4

禁止使用前一个 SKU 变体继续生成下一个 SKU。

---

## 8. BUILD_SKU_SET

流程：
1. 指定母版 SKU
2. 生成第 1 张独立候选
3. 停止
4. 用户需要时继续逐张生成其他候选
5. 用户选择 ORIGINAL MASTER
6. 锁定 ORIGINAL MASTER
7. 其他 SKU 全部直接从 ORIGINAL MASTER 生成

未选择正式母版前，不得提前生成其他 SKU。

---

## 9. Logo 原子化保护

上传 Logo 是不可拆分的完整图形。

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

Logo 内文字不是可编辑文字。

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

## 10. Logo 位置与尺寸

1200 × 1600 px：
- 左边距 ≥ 60 px
- 上边距 ≥ 80 px
- Logo 完整位于画布内

最大包围框：
- 宽度 ≤ 220 px
- 高度 ≤ 100 px

保持原始宽高比。

候选之间 Logo 视觉尺寸保持一致。

ORIGINAL MASTER 选定后：
- Logo 位置锁定
- Logo 尺寸锁定

---

## 11. 信息区

Logo + 产品名称 + 版本文字组成稳定信息区。

必须：
- 产品名称位于 Logo 下方
- 产品名称与版本文字位于上半部分
- 标题优先与 Logo 形成统一视觉左轴
- 版本文字与标题左对齐
- Logo → 标题间距合理
- 标题 → 版本间距合理
- 信息区不得侵入产品核心展示区

长标题：
- 优先一行
- 最多两行
- 不得从单词中间断开
- 可适度缩小字号
- 信息区仍须保持在上半部分

ORIGINAL MASTER 选定后锁定：
- 标题位置
- 版本位置
- 左轴关系
- Logo → 标题间距
- 标题 → 版本间距
- 信息区整体结构

---

## 12. 产品 PNG 保护

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
- 自然接触阴影
- 克制的环境阴影
- 必要的轻微分离光

---

## 13. 允许出现的内容

只允许：
1. 上传品牌 Logo
2. 精确产品名称
3. 精确版本文字
4. 上传产品 PNG
5. Classic M3 视觉元素
6. 服务于层级关系的自然光影

产品自身真实存在的文字和屏幕内容可保留。

禁止新增：
- 卖点
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

## 14. Typography

产品名称：
- 现代中性无衬线
- Google Sans / Roboto / Material-like
- Bold 700
- 主要文字层级
- 优先一行
- 最多两行

版本文字：
- Medium 500
- 清晰可读
- 次级文字层级
- 不得过小或像脚注

---

## 15. Classic M3 视觉框架

### Color
使用 tonal relationships 组织：
- Surface 区分
- 层级
- 产品与背景分离
- 视觉节奏

不使用固定颜色表。
不使用固定“产品颜色 → 背景颜色”映射。
具体 hue 自适应。

### Shape
Shape 用于组织：
- 构图
- 注意力
- Surface 关系
- 产品与背景关系

不规定必须使用某一种 Shape。

### Surface
背景优先理解为具有层级关系的视觉 Surface。

Surface 可用于：
- 分区
- 承托
- 层级
- tonal 关系
- 视觉节奏

不要求模拟真实物理空间。

### Elevation
通过：
- tonal difference
- soft shadow
- overlap
- subtle depth

表达层级。

Elevation 是视觉层级工具，不等于写实建筑空间。

### Typography
通过字号、字重、位置和间距建立稳定信息层级。

---

## 16. 静态产品视觉适配

核心：

**Graphic-first, depth-second**

先建立：
- Surface 结构
- Shape 关系
- tonal relationships
- 信息层级

再加入：
- 克制的空间深度
- 柔和 Elevation
- 产品真实光影

产品保持真实。

设计环境保持足够图形化，使画面首先呈现为 Classic M3 构成，而不是高写实棚拍或建筑空间。

具体：
- 构图
- 配色
- Shape
- Surface
- 产品位置
- 空间关系

由当前产品独立决定。

---

## 17. 缩略图可读性

缩小显示时：
- 产品主体仍容易识别
- 产品与背景保持清晰分离
- 产品名称保持基本可读
- 信息层级明确
- 构图完整

这里只限制可读性，不规定具体构图、场景或展示结构。

---

## 18. SKU 结构锁定

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
- Shape 结构
- Surface 结构
- 背景几何大小
- 背景几何位置
- 整体构图
- 基本光源方向

不得重新设计版式。

---

## 19. SKU 自适应配色

每个 SKU 独立重新评估：
- 背景主色
- Surface tonal relationships
- Shape 填充色
- 阴影强弱
- 必要的轻微分离光
- 必要的文字明暗

不继承前一个 SKU 的配色偏好。

核心：

**锁定结构，自适应配色。**

---

## 20. SKU 背景区分

同一产品不同颜色 SKU 的背景必须具有明显视觉区分。

每生成一个新 SKU，都要与同一套已确认 SKU 的背景进行比较。

不得重复：
- 相同背景主色
- 高度接近的 hue family
- 高度接近的 tonal palette
- 仅靠轻微明暗调整产生的“差异”

缩略图并排显示时，背景应能快速区分。

同时：
- 保持 Classic M3 tonal harmony
- 保持产品与背景分离
- 不为了区分而使用随意冲突色
- 不通过改变布局或几何结构制造 SKU 差异

若背景过于相近：
- 保持锁定结构
- 重新计算当前 SKU palette
- 再次验证

不使用固定颜色映射表。

---

## 21. POST-GENERATION VALIDATION

交付前必须验证。

### 硬验证
确认：
- 当前回合只生成 1 张
- 严格 portrait 3:4
- 不是通过裁切其他比例得到
- 目标为 1200 × 1600 px，或来自严格 3:4 且可无裁切等比例缩放的源图
- Logo 与上传源素材一致
- 产品与上传源素材一致
- 产品名称准确
- 版本文字准确
- 无额外文字 / 图标 / 徽章

任何一项失败：
- 当前输出视为无效
- 不得作为有效候选交付

### 母版候选额外验证
- 当前回合只有 1 张独立候选
- 无拼版
- 当前候选从原始输入重新独立设计

### SKU 额外验证
- Image A 是 ORIGINAL MASTER
- Logo 与信息区保持锁定
- 产品视觉中心与尺寸逻辑一致
- Shape / Surface 结构保持锁定
- 当前 SKU palette 独立评估
- 当前 SKU 背景与同套其他 SKU 明显区分

只有通过验证的输出才算有效结果。
