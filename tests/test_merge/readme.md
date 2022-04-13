- 构造A B两个版本基于 `3918b7a3aec0` 同时开发，都创建了 `3918b7a3ae10、3918b7a3ae11` 两个版本文件，而且他们的 `down_revision 和 revision` 值都一样

```s
A: 3918b7a3aec0 --> 3918b7a3ae10 --> 3918b7a3ae11
B: 3918b7a3aec0 --> 3918b7a3ae10 --> 3918b7a3ae11
要求支持A --> B
```

- 尝试使用 `alembic merge` 的方法支持A版本升级到B版本，实际操作时报错
  ```sh
  # 执行合并
  $alembic merge -m "merge 3918b7a3ae10_add_column_address2 3918b7a3ae10_add_column_address" 3918b7a3ae10 3918b7a3ae10
  # 失败
  FAILED: Duplicate head revisions specified
  
  # 原因是现在使用的是递增的版本序号，而不是由 alembic 自动生成的，所以序号重复就直接报错了，如果序号不重复倒是可以试试 merge 的方法
  ```
