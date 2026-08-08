# BUILD_SKU_SET

流程：

1. 指定母版 SKU
2. 单回合生成 1 张独立母版候选
3. 需要更多候选时逐张继续
4. 用户选择 ORIGINAL MASTER
5. 锁定 ORIGINAL MASTER
6. 其他 SKU 全部直接从 ORIGINAL MASTER 生成
7. 每个 SKU 独立计算 palette
8. 不同 SKU 的背景必须明显区分
9. 禁止 SKU 链式派生

每次生成都执行：

PREFLIGHT → GENERATE → VALIDATE
