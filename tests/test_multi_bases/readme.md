
- 生成脚本的时候指明版本和分支
  ```s
  # 修改 alembic.ini 说明升级脚本路径
  version_locations = %(here)s/migration/versions/BBC2.5.6 migration/versions

  # 执行命令自动创建BBC2.5.6版本文件夹，并且按照 script.py.mako 模板生成升级脚本
  $ alembic revision -m "create post table" --head=base --branch-label=BBC2.5.6 --version-path=migration/versions/BBC2.5.6

  # 后续创建升级脚本的时候，如果指定头，会自动放到对应的文件夹下
  $ alembic revision -m "add test column" --head=BBC2.5.6

  $ alembic upgrade heads # 会把各个分支下的脚本执行，查看alembic_version可以看到每个版本都有一条记录
  ```

- 分支之间的依赖
