# BUILD_SKU_SET

用于同一产品多个 SKU。

流程：

1. 指定母版 SKU
2. 只使用母版 SKU 生成 5 个独立候选
3. 停止
4. 等待用户选择 ORIGINAL MASTER
5. 锁定 ORIGINAL MASTER
6. 其他 SKU 全部直接从 ORIGINAL MASTER 生成

正确：

ORIGINAL MASTER + SKU 2
ORIGINAL MASTER + SKU 3
ORIGINAL MASTER + SKU 4

错误：

MASTER → SKU 2 → SKU 3 → SKU 4

所有 SKU：

- 严格 3:4
- 目标尺寸 1200 × 1600
- Logo 原子化保护
- 产品 PNG 保护
- 信息区锁定
- 背景几何结构锁定
- 当前 SKU 配色独立重新评估

不使用固定配色模板。
不使用固定视觉情绪模板。

核心：

锁定结构，自适应配色。
