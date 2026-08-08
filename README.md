# md3-product-main-image

用于生成电商产品主图的标准 Codex Skill。它只采用 Google Classic
Material Design 3，并通过一张用户确认的 `ORIGINAL MASTER` 保持同款不同
SKU 的版式一致。

## 文件结构

```text
md3-product-main-image/
├── SKILL.md
└── README.md
```

没有 `references/`、`prompts/`、`scripts/` 或 `agents/` 目录。Classic M3
不再由额外参考文件解释，全部必要执行规则都在 `SKILL.md` 中。

## 核心工作流

1. 用品牌 Logo、产品 PNG、准确的产品名称和版本文字生成一张母版候选。
2. 每轮只生成一张；需要下一张时，从原始素材重新独立设计。
3. 用户明确选择后，该图才成为 `ORIGINAL MASTER`。
4. 每个后续 SKU 都直接由 `ORIGINAL MASTER + 当前 SKU PNG` 生成，禁止链式派生。

## 当前 Logo 与文字原则

- Logo 是不可拆分、不可重绘的受保护素材，只允许等比例缩放和定位。
- Logo 的透明区保持透明语义，不得生成底板、矩形补丁或局部修复接缝。
- 约 60 px 左边距、80 px 上边距和 220 x 100 px 最大可见尺寸仅是视觉参考，
  不是像素级硬校验。
- Logo 不得小到难以识别，也不得过大、贴边或被裁切。
- 母版候选之间不强制 Logo 尺度一致；选定母版后才锁定。
- Logo、产品名称和版本文字作为一个完整信息组，形成清晰的视觉左轴，
  但不使用 `INFO_X` 或数学式坐标校验。
- 产品名称与版本文字必须逐字准确；字体、字重、间距和换行按视觉层级判断，
  不再强制指定字体名或 700/500 等 CSS 式数值。
- 硬约束失败时整张作废并从原始输入重生成，不做局部补丁。

## 使用示例

创建母版候选：

```text
使用 md3-product-main-image。

产品名称：Xiaomi Smart Scale S200
版本文字：Глобальная версия

当前上传的是品牌 Logo 和母版 SKU 产品 PNG。
进入 CREATE_MASTER_OPTIONS。
```

继续探索：

```text
继续生成下一张独立母版候选。
```

确认母版：

```text
将当前方案设为 ORIGINAL MASTER。
```

替换 SKU：

```text
Image A 是 ORIGINAL MASTER。
Image B 是当前 SKU 的原始产品 PNG。
进入 REPLACE_VARIANT。
```

## 画布与交付

- 每轮正好一张独立图片
- 竖版 3:4
- 目标尺寸 1200 x 1600 px
- 禁止从其他比例裁切为 3:4
- 仅当源图本身严格为 3:4 时，允许不裁切的等比例缩放
