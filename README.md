# MD3 Product Main Image Skill v3.2

GPT-image-only workflow for premium e-commerce product main images.

No Photoshop. No PSD. No external compositing. No website workflow.

## v3 核心变化

- 每个新产品先生成 5 个母版候选
- 用户明确选择其中 1 个后才锁定母版
- 支持单个 SKU 替换
- 支持批量 SKU
- 品牌 Logo 作为受保护素材，不允许修改
- 产品 PNG 作为受保护素材，不允许修改
- 禁止生成“相似但不完全相同”的 Logo 或产品替代版本
- 所有 SKU 始终从 ORIGINAL MASTER 派生

## 新产品流程

CREATE_MASTER_OPTIONS → 生成 5 个 → STOP → 用户选择 → SELECT_MASTER → MASTER_APPROVED

## 单个变体

ORIGINAL MASTER + 上传 SKU PNG → REPLACE_VARIANT

## 批量 SKU

母版颜色 SKU → 5 个候选 → 用户选择 → 锁定 ORIGINAL MASTER → ORIGINAL MASTER + SKU 2 / SKU 3 / SKU N

绝不链式编辑变体。

## 示例

上传 Logo + 黑色产品 PNG，然后说：

产品名称：Redmi Watch 6
版本：Глобальная версия
黑色作为母版。
生成 5 个 MD3 母版方案供我选择。

生成 5 个后必须停止。

你回复：

方案 3，就用这个。

此时 OPTION 3 = MASTER_SELECTED，MASTER_APPROVED = true。

如果还上传了蓝色和白色 PNG，后续应分别执行：

ORIGINAL MASTER + 蓝色 PNG
ORIGINAL MASTER + 白色 PNG

## 受保护素材原则

工作流可以改变：位置、等比例大小、背景、构图、光影、阴影。

工作流不得改变：Logo 图形、Logo 颜色、Logo 比例、产品身份、产品结构、产品颜色、产品物理细节。

构图适应素材，素材不为了构图而被重构。
