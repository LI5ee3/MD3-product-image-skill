# md3-product-image

生成 3:4 Google Classic MD3 电商产品图。Image Gen 只生成空背景；透明产品 PNG、固定 50° 二维投影、源 Logo 和 Roboto Bold 文字均在本地合成。母版由用户确认，SKU 自动沿用已绑定布局。

运行环境：Python 3.10+、Pillow。

## 使用

上传透明产品 PNG 和透明 Logo PNG：

```text
使用 $md3-product-image

完整产品名称：[完整名称]
品牌：[品牌]
品牌以外的产品名称或型号：[其余名称]
产品名称显示行数：[一行/两行]
品牌 Logo 类型：[图形/文字]
版本文字：[可选；无则删除本行]

创建一个母版候选
```

确认候选：

```text
使用 $md3-product-image 将候选 [候选 ID] 设为母版
```

生成 SKU：

```text
使用 $md3-product-image

产品文件夹：[绝对路径]

使用当前上传的透明产品 PNG 生成 SKU 变体
```

`产品名称显示行数`和`品牌 Logo 类型`必须手动填写。SKU 自动命名为 `SKU_VARIANT-A`、`SKU_VARIANT-B`……。

## 输出

每个产品使用独立文件夹。`output` 只保存 `ORIGINAL_MASTER_FINAL.png` 和最终 `SKU_VARIANT-*.png`；其他工作文件保存在产品文件夹根目录。

## Roboto Bold 字体许可证

`assets/Roboto-Bold.ttf`：

```text
Copyright 2011 The Roboto Project Authors
```

字体采用 SIL Open Font License 1.1：可以使用、嵌入、修改和再分发，但不得单独销售；再分发时须保留版权声明和许可证。使用该字体生成的图片不受字体许可证继承要求约束。

完整许可证见 [`assets/OFL.txt`](assets/OFL.txt)。
