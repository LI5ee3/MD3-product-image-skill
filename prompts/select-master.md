# SELECT_MASTER

只在用户明确选择某个候选后执行。

例如：

- 方案3
- 第三张作为母版
- 选第3个
- 方案3，就用这个

然后：

MASTER_SELECTED = selected original candidate
MASTER_APPROVED = true

选中的原始候选图成为唯一 ORIGINAL MASTER。

后续 SKU 必须直接使用这个 ORIGINAL MASTER。

不要：

- 混合其他候选
- 重新生成“类似母版”
- 使用其他候选作为 SKU 来源
