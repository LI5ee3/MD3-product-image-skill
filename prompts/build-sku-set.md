# BUILD COMPLETE SKU SET

请为当前产品生成一整套同款不同颜色 SKU 电商主图。

必须使用“5 个母版候选 → 用户选择 → 锁定母版 → 逐个替换 SKU”的流程。

禁止分别独立设计每一种颜色。

## Image Ratio Rule

整套 SKU 图片必须全部使用固定 3:4 比例。

目标尺寸统一为：

1200 × 1600 px

这包括：

- 5 个母版候选
- 最终选定母版
- 每一个颜色 SKU 变体

不得生成任何非 3:4 图像。

不得先生成其他比例再裁切成 3:4。

# Input

产品名称：{{PRODUCT_NAME}}
版本：{{VERSION_TEXT}}
品牌 Logo：使用上传 Logo。
SKU 产品 PNG：{{SKU_IMAGES}}
母版颜色：{{MASTER_SKU}}

如果用户指定母版颜色，必须使用指定颜色。

# 最高优先级：素材保护

每一个上传 SKU PNG 都是受保护源素材。不得根据其他颜色 SKU 自行生成近似颜色版本。必须使用对应上传 PNG。

品牌 Logo 同样受保护，不得修改。



# Atomic Logo Rule

整套 SKU 中，上传的品牌 Logo 必须始终被视为一个不可拆分的整体图形。

Logo 内部所有字母、Wordmark、品牌名称文字均属于 Logo 图形本身。

不得：

- OCR 后重新打字
- 重新排版 Logo 内文字
- 修改字形、字距或字重
- 拆分图形标与文字标
- 在某些 SKU 中重新生成相似 Logo

5 个母版候选和全部最终 SKU 都必须保留同一个完整 Logo 图形。

只有产品名称和版本文字属于可生成文本。

# Logo 固定区域

整套 SKU 的品牌 Logo 必须始终位于左上角安全区。

对于 1200 × 1600 px：

- 左边安全距离至少 60 px
- 上边安全距离至少 80 px
- Logo 不得离开左上区域
- 所有母版候选与最终 SKU 都必须遵守

不得通过改变 Logo 位置制造不同母版构图。


# Logo 大小一致性

整套 SKU 中的 Logo 必须保持统一视觉尺寸。

对于 1200 × 1600 px：

- Logo 最大包围框：220 × 100 px
- 必须保持原始宽高比
- 不得拉伸、压缩、裁切或变形

在 5 个母版候选中：

- Logo 大小保持一致
- Logo 位置保持左上安全区规则
- 不允许通过改变 Logo 尺寸来制造候选方案差异

母版选定后：

- Logo 宽度锁定
- Logo 高度锁定
- Logo 位置锁定

所有后续 SKU 必须与 ORIGINAL MASTER 保持一致。

# 母版候选独立输出规则

批量 SKU 模式的母版探索阶段也必须遵守：

5 个母版候选 = 5 张独立图片。

不得生成：

- 五宫格
- 拼版
- Contact Sheet
- Collage
- Grid
- Multi-panel

必须按顺序逐张生成：

MASTER OPTION 1
→ 单独 3:4 图片

MASTER OPTION 2
→ 单独 3:4 图片

MASTER OPTION 3
→ 单独 3:4 图片

MASTER OPTION 4
→ 单独 3:4 图片

MASTER OPTION 5
→ 单独 3:4 图片

然后：

STOP
→ WAIT FOR USER SELECTION

如果当前界面不能在一次回复中生成 5 张独立图片，
先生成 OPTION 1 后停止，等待用户继续。

不得用一张拼版图代替 5 张独立候选。


# PHASE 1 — MASTER EXPLORATION

仅使用 {{MASTER_SKU}} 执行 CREATE_MASTER_OPTIONS，生成 5 个真正不同构图方向的 MD3 母版候选。

生成后 STOP。不得继续生成其他 SKU，等待用户选择方案 1–5。

# PHASE 2 — MASTER SELECTION

用户选择后：selected option = MASTER_SELECTED；MASTER_APPROVED = true。

只使用用户选中的 ORIGINAL MASTER。其他候选从生产流程排除。

# PHASE 3 — SKU PRODUCTION

对于每一个剩余 SKU：

Image A = ORIGINAL MASTER
Image B = 当前 SKU 对应的上传 PNG

按照 REPLACE_VARIANT 规则生成。

正确：MASTER + BLACK / MASTER + BLUE / MASTER + WHITE / MASTER + PINK

错误：BLACK → BLUE → WHITE → PINK

# SKU 之间允许

- 上传产品 PNG 不同
- 背景主题色不同
- MD3 几何配色不同
- 阴影强弱适配
- 文字明暗适配

# SKU 之间不允许

- Logo 漂移或改样
- 标题/版本漂移
- 产品大小/中心漂移
- 背景几何尺寸/位置变化
- 重新设计构图
- 修改上传产品外观

最终整组图片应像同一个设计模板在切换上传 SKU，而不是多张分别重新设计的海报。
