# Execution Contract

所有生成执行：

PREFLIGHT → GENERATE → VALIDATE

## PREFLIGHT
生成前确认：
- exactly 1 image
- portrait 3:4
- target 1200 × 1600 px
- no substitute ratio
- no crop-to-fit workflow
- source Logo present
- source product PNG present
- exact product name known
- exact version text known

若 exact 3:4 无法保证，停止生成。

## GENERATE
只有 PREFLIGHT 通过后才生成。

## VALIDATE
交付前验证：
- 1 image
- 3:4 portrait
- no crop from another ratio
- correct Logo
- correct product
- exact text
- no extra content

不合格输出不计为有效候选。
