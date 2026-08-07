# BUILD COMPLETE SKU SET

请为当前产品生成一整套同款不同颜色 SKU 电商主图。

必须使用“5 个母版候选 → 用户选择 → 锁定母版 → 逐个替换 SKU”的流程。

禁止分别独立设计每一种颜色。

## Input

产品名称：{{PRODUCT_NAME}}
版本：{{VERSION_TEXT}}
品牌 Logo：使用上传 Logo。
SKU 产品 PNG：{{SKU_IMAGES}}
母版颜色：{{MASTER_SKU}}

如果用户指定母版颜色，必须使用指定颜色。

# 最高优先级：素材保护

每一个上传 SKU PNG 都是受保护源素材。不得根据其他颜色 SKU 自行生成近似颜色版本。必须使用对应上传 PNG。

品牌 Logo 同样受保护，不得修改。

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
