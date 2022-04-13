
- 测试两个有相同 `down_revision` 的升级脚本
  ```s
  $ alembic heads
  vabc256seq001 (head)
  vabc256seq002 (head)

  $ alembic upgrade heads

  # 数据库出现了两个版本号
  # 查看表结构，这两个脚本都已经执行了
  MySQL > select * from alembic_version;
  +---------------+
  | version_num   |
  +---------------+
  | vabc256seq001 |
  | vabc256seq002 |
  +---------------+

  # 降级的话，会从 version_num 表里删除一条记录
  $ alembic downgrade -1
  MySQL > select * from alembic_version;
  +---------------+
  | version_num   |
  +---------------+
  | vabc256seq002 |
  +---------------+

  $ alembic downgrade -1
  MySQL > select * from alembic_version;
  +---------------+
  | version_num   |
  +---------------+
  | 3918b7a3aec0  |
  +---------------+
  ```
