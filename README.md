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
将这张图设为ORIGINAL MASTER
```

确认母版后生成其他SKU：

```text
根据已设定的ORIGINAL MASTER
使用当前上传的产品图生成这个SKU
根据当前SKU重新推导背景配色，同时保持母版结构、构图、光影方向和信息组不变
```
