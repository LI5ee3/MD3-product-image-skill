# md3-product-image

生成 3:4 Google Classic MD3 电商产品图<br>Image Gen 只生成空背景；透明产品 PNG、固定 50° 二维投影、源 Logo 和 Roboto Bold 文字均在本地合成<br>母版由用户确认，SKU 自动沿用已绑定布局

运行环境：Python 3.10+、Pillow

## 使用

```text
使用 md3-product-image
完整产品名称：[完整名称]
品牌：[品牌]
品牌以外的产品名称或型号：[其余名称]
产品名称显示行数：[一行/两行]
品牌 Logo 类型：[图形/文字]
版本文字：[可选] 
生成母版
```

确认候选：

```text
锁定母版
```

重做母版：

```text
重做母版：[可选追加提示词]
```

生成 SKU：

```text
使用当前产品图生成 SKU
```

确认或重做 SKU：

```text
确认当前 SKU
```

```text
重做当前 SKU：[可选追加提示词]
```

`产品名称显示行数`和`品牌 Logo 类型`必须手动填写<br>每次只生成一张完整预览，母版和 SKU 均由用户确认<br>SKU 自动命名为 `SKU_VARIANT-A`、`SKU_VARIANT-B`……

## 输出

每个产品使用独立文件夹<br>`reusable` 保存布局、累计提示词和可复用合成资产<br>`output` 只保存 `ORIGINAL_MASTER_FINAL.png` 和已确认的 `SKU_VARIANT-*.png`<br>其他工作文件保存在产品文件夹根目录

## Roboto Bold 字体许可证

`assets/Roboto-Bold.ttf`：

```text
Copyright 2011 The Roboto Project Authors
```

字体采用 SIL Open Font License 1.1：可以使用、嵌入、修改和再分发，但不得单独销售；再分发时须保留版权声明和许可证。使用该字体生成的图片不受字体许可证继承要求约束

完整许可证见 [`assets/OFL.txt`](assets/OFL.txt)
