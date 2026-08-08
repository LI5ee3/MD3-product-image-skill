# md3-product-image

生成Google Classic MD3风格的3:4电商产品主图<br>
产品与场景统一生成，原始Logo和指定文字保持准确，并支持母版确认后的同款SKU替换

## 使用

上传产品图作为 Image 1、原始 Logo PNG 作为 Image 2，然后发送：

```text
使用md3-product-image

完整产品名称：[完整名称]
品牌：[品牌]
品牌以外的产品名称或型号：[其余名称]
版本文字：[版本文字；不需要时省略这一行]

创建一个母版候选
```

确认母版后生成其他 SKU：

```text
将这张图设为ORIGINAL MASTER
使用当前上传的产品图生成这个SKU，并保持母版构图和信息组不变
```
