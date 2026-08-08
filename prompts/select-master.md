# SELECT_MASTER

当用户明确选择某一候选时：

将该原始候选锁定为唯一 ORIGINAL MASTER。

例如：

- 方案3作为 ORIGINAL MASTER
- 选第3张
- 第三张作为正式母版

后续所有 SKU 必须直接从该 ORIGINAL MASTER 派生。

不得混合其他候选。
不得重新生成一个“相似母版”作为替代。
