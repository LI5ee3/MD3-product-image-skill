# BUILD COMPLETE SKU SET

请为当前产品生成一整套同款不同颜色 SKU 电商主图。

必须使用：

“先母版 → 后逐个替换”

的流程。

禁止分别独立设计每一种颜色。

## Input

产品名称：

{{PRODUCT_NAME}}

版本：

{{VERSION_TEXT}}

品牌 Logo：

使用上传 Logo。

SKU 产品 PNG：

{{SKU_IMAGES}}

母版颜色：

{{MASTER_SKU}}

如果用户已经指定母版颜色，必须使用指定颜色。

## STEP 1 — MASTER

首先仅使用母版颜色 PNG：

{{MASTER_SKU}}

根据 CREATE_MASTER 规则创建一张 1200 × 1600 px MD3 母版。

这一步确定并锁定：

- Logo
- 产品名称
- 版本
- 产品大小
- 产品中心
- 背景几何结构
- 构图
- 光影方向

## STEP 2 — LOCK

母版生成后，将其作为唯一的版式来源。

不得为后续颜色重新构图。

## STEP 3 — SKU REPLACEMENT

对于每一个剩余 SKU：

使用：

Image A = 母版

Image B = 当前颜色 PNG

按照 REPLACE_VARIANT 规则生成。

每一个颜色都必须从同一张母版派生。

不要使用前一个变体作为下一个变体的母版。

始终使用最初确认的 MASTER。

正确：

MASTER + BLACK
MASTER + BLUE
MASTER + WHITE

错误：

BLACK → BLUE → WHITE

避免连续编辑造成构图漂移。

## Allowed Differences

SKU 之间允许：

- 产品颜色不同
- 背景主题色不同
- MD3 几何配色不同
- 阴影强弱适配
- 文字明暗适配

SKU 之间不允许：

- Logo 漂移
- 标题漂移
- 版本漂移
- 产品大小漂移
- 产品中心漂移
- 背景几何尺寸变化
- 背景几何位置变化
- 重新设计构图

## Final Visual Goal

把全部 SKU 快速连续查看时，应感觉：

同一个设计模板在切换产品颜色。

而不是：

多张不同设计师分别完成的海报。
