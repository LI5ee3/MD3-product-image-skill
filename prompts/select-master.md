# SELECT MASTER

用户正在从 5 个母版候选方案中选择正式母版。

识别明确选择，例如：

- “方案3” → OPTION 3
- “第二张” → OPTION 2
- “选第五个” → OPTION 5
- “一号做母版” → OPTION 1
- “方案3不错，就用这个” → OPTION 3

选择明确后：

1. 将对应原始候选图标记为 MASTER_SELECTED。
2. 设置 MASTER_APPROVED = true。
3. 后续所有同款 SKU 必须直接使用该原始候选图作为 Image A。
4. 不得混入其他候选方案元素。
5. 不得再自行改变母版构图。
6. 如果当前处于 BUILD_SKU_SET，才可以继续处理剩余 SKU。

如果用户只是评价某个方案但没有明确选择，不要擅自锁定。

如果用户要求重新生成五个方案，则返回 CREATE_MASTER_OPTIONS，在新母版选择前不得继续 SKU 生产。
