# MD3-product-image

生成Google Classic MD3风格的3:4电商产品主图<br>产品与场景统一生成，原始Logo和指定文字保持准确，并支持母版确认后的同款SKU替换

## 使用

上传产品图作为Image 1、原始Logo PNG作为Image 2，然后发送：

```text
使用 md3-product-image

完整产品名称：[完整名称]
品牌：[品牌]
品牌以外的产品名称或型号：[其余名称]
版本文字：[版本文字；不需要时省略这一行]

创建一个母版候选
```

确认母版：

```text
将这张图设为ORIGINAL MASTER，并在本组 SKU 中保持不变
```

之后每次生成其他SKU：

```text
继续使用当前已锁定的同一ORIGINAL MASTER
使用当前上传的产品图生成这个SKU
根据当前SKU重新推导背景配色，同时保持母版结构、构图、光影方向和信息组不变
将输出作为SKU_VARIANT，不能替换、覆盖或重新锁定为ORIGINAL MASTER
```
