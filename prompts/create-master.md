【输入】

品牌 Logo：
使用我上传的品牌 Logo。

产品 PNG：
使用我上传的当前产品 PNG。

产品名称：
{{产品名称}}

版本文字：
{{版本文字}}

【任务】

使用 md3-product-main-image。

进入 CREATE_MASTER_OPTIONS。

当前回合只生成 1 张独立母版候选图。

必须执行：

PREFLIGHT → GENERATE → VALIDATE

PREFLIGHT：
- 只输出 1 张
- 严格 portrait 3:4
- 目标 1200 × 1600 px
- 不允许其他比例替代
- 不允许先生成其他比例再裁切
- Logo、产品 PNG、产品名称、版本文字均已确认

如果无法保证严格 3:4，不要生成无效候选。

设计只使用 Classic Material Design 3。

当前候选必须从原始输入重新独立设计，
不要把之前候选作为修改基础。

生成后必须通过 VALIDATE 才算有效候选。
