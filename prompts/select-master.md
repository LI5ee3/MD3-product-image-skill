# SELECT_MASTER

当用户明确选择某一候选时：

将该原始候选锁定为唯一 ORIGINAL MASTER。

后续所有 SKU 必须直接从该 ORIGINAL MASTER 派生。

不得混合其他候选。
不得重新生成一个“类似母版”替代 ORIGINAL MASTER。
