# MD3 产品主图 Skill v6.4

v6.4 是按**标准 Skill**思路重新简化后的完整重构版本。

不再为普通聊天单独制作 Standalone Prompt，也不再保留聊天专用工作流文件。

## 核心方向

只使用：

> **Classic Material Design 3**

核心视觉目标：

> **真实产品 + 图形化 Classic M3 环境**

核心原则：

> **Graphic-first, depth-second**

## 核心硬约束

- 单回合只生成 1 张母版候选
- portrait 3:4
- 目标 1200 × 1600 px
- 不允许其他比例替代后裁切
- Logo 原子化保护
- 产品 PNG 保护
- Logo / 产品名称 / 版本文字组成 Atomic Information Zone
- 使用统一 `INFO_X` 左轴
- 禁止对 Logo、产品、信息区做局部后期修补
- 硬约束失败时整张重新生成
- ORIGINAL MASTER 锁定
- SKU 不链式派生
- 同一产品不同 SKU 的背景必须明显区分

## Classic M3

不把 Classic M3 做成固定模板。

重点使用：

- Color
- Shape
- Surface
- Elevation
- Typography

其中：

- Surface 主要理解为图形化视觉层
- Elevation 主要理解为图层层级
- 产品保持真实
- 环境保持图形化、简化、tonal、结构化

## 文件结构

```text
md3-product-main-image-v6.4/
├── SKILL.md
├── README.md
└── references/
    └── classic-m3-principles.md
```

## 使用方式

加载整个 Skill 后直接描述当前任务即可。

例如：

```text
使用 md3-product-main-image。

产品名称：Xiaomi Smart Scale S200
版本文字：Глобальная версия

当前上传的 Logo 为品牌 Logo。
当前上传的产品 PNG 作为母版 SKU。

进入 CREATE_MASTER_OPTIONS。
```

继续下一张候选：

```text
继续生成下一张独立母版候选。
```

选择母版：

```text
方案 3 作为 ORIGINAL MASTER。
```

替换 SKU：

```text
Image A 是 ORIGINAL MASTER。
Image B 是当前 SKU 产品 PNG。

进入 REPLACE_VARIANT。
```

## 版本维护原则

后续每次更新：

- 重新整合完整 Skill
- 删除被新规则替代的旧表达
- 避免重复规则
- 避免补丁式累积
- 保持硬约束明确、创意规则简洁
