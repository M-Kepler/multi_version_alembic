- [使用举例](#使用举例)
- [改动说明](#改动说明)
- [多版本并行开发](#多版本并行开发)
    - [多分支](#多分支)
        - [按版本归档](#按版本归档)
        - [分支合并](#分支合并)
    - [添加迁移脚本规范](#添加迁移脚本规范)
- [其他](#其他)
    - [`alembic` 基础命令](#alembic-基础命令)

# 使用举例

- 使用说明

    ```sh
    $python db_assit.py

    usage: db_assist.py [-h] [-t {init,upgrade,help}] [-y]

    optional arguments:
      -h, --help            show this help message and exit
      -t {init,upgrade,help}, --type {init,upgrade,help}
                            operation type
      -y                    do it, without any warning
    ```

- 开始数据库脚本迁移

    ```sh
    $python db_assist.py -t init

    Warning: database already exists, this action will erase all data!!!
    Continue init database? (y/n): y

    mysql: [Warning] Using a password on the command line interface can be insecure.
    INFO  [alembic.runtime.migration] Context impl MySQLImpl.
    INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
    INFO  [alembic.runtime.migration] Running upgrade  -> 3918b7a3aec0, create account table
    ------in base@head
    INFO  [alembic.runtime.migration] Running upgrade  -> v256seq001, add column address
    ------in 2.5.6@head sequence 001
    INFO  [alembic.runtime.migration] Running upgrade v256seq001 -> v256seq002, add column email
    ------in 2.5.6@head sequence 002
    INFO  [alembic.runtime.migration] Running upgrade  -> v257seq001, add column address
    ------in 2.5.7@head sequence 001
    INFO  [alembic.runtime.migration] Running upgrade v257seq001 -> v257seq002, add column age
    ------in 2.5.7@head sequence 002

    ```

- 查看完成迁移后的数据库版本号

    ```sql
    mysql> select * from alembic_version;
    +--------------+
    | version_num  |
    +--------------+
    | 3918b7a3aec0 |   -----> 这是 没有归到版本里的，基础脚本编号
    | v256seq002   |   -----> 这是 256 版本的最新迁移脚本编号
    | v257seq002   |   -----> 这是 257 版本的最新迁移脚本编号
    +--------------+
    ```

- 查看完成迁移后的版本链

    ```sh
    $alembic heads

    # 三个版本分支
    v257seq002 (2.5.7) (head)
    v256seq002 (2.5.6) (head)
    3918b7a3aec0 (head)


    $alembic history

    # 执行完 256 文件夹下的升级脚本后，就执行 257 下的升级脚本
    # 这正是我们要的，脚本按版本存放，且按顺序执行

    # 2.5.7 这一条分支的升级路径
    v257seq001 -> v257seq002 (2.5.7) (head), add column age
    <base> -> v257seq001 (2.5.7), add column address

    # 2.5.6 这一条分支的升级路径
    v256seq001 -> v256seq002 (2.5.6) (head), add column email
    <base> -> v256seq001 (2.5.6), add column address
    # head 这一条分支的升级路径
    <base> -> 3918b7a3aec0 (head), create account table


    # 查看 2.5.6 分支的升级历史
    $alembic history -r 2.5.6:

    v256seq001 -> v256seq002 (2.5.6) (head), add column email
    <base> -> v256seq001 (2.5.6), add column address


    # 查看从基准分支升级上来的历史记录
    $alembic history -r :2.5.6@head

    v256seq001 -> v256seq002 (2.5.6) (head), add column email
    <base> -> v256seq001 (2.5.6), add column address


    # 查看部分历史
    $alembic history -r :2.5.6@head-1

    <base> -> v256seq001 (2.5.6), add column address
    ```

# 改动说明

[看合并请求]

# 多版本并行开发

- [官方文档](https://alembic.sqlalchemy.org/en/latest/branches.html)

其实可以这样啊，简单解决，每个版本的数据库脚本文件就放到各自的文件夹下，然后执行升级的时候，不是一次升级到最新 `alembic upgrade head` 而是一个个脚本执行 `alembic upgreade [script_num]`，如果脚本序号是哈希的倒也还好，可是现在是按顺序排列的。这样的话没办法解决两个版本含有同一个脚本序号的问题

## 多分支

- 测试每个版本各自建立一个文件夹存放该版本的升级脚本，各自排序，每个脚本填补上 `branch_labels` 属性表示该脚本属于那个版本的

- 版本分支情况

    ```sh
    A: # 版本文件夹
        A0001_add_column.py  #  branch_labels = "A" 该版本第一个脚本指定 branch_labesl 即可
        A0002_add_column.py
    B:
        B0001_add_column.py  #  branch_labels = "B"
        B0002_add_column.py
    ```

- 如果分支版本中添加了 `branch_labels` 的话，想新建升级脚本就要指定分支，否则无法新建

    ```sh
    # 一个脚本中声明了 branch_labels
    $alembic revision -m "test"

    # 报错
    FAILED: Multiple heads are present; please specify the head revision on which the new revision should be based, or perform a merge.

    # 生成时指定分支 A
    $alembic revision -m "test" --head A@head

    $alembic history
    # 虽然查看生成的脚本中 branch_labels 还是None，但是通过命令来看可以追溯到它所在的分支
    # 所以如果想给某个分支新建多个升级脚本，不要每个脚本都指明 [branch_label]，只要第一个指明就行了，后续的根据 revision 和 down_revision 可以跟踪到它属于哪个分支
    vabc256seq001 -> cd7de7e6dddd (A) (head), test
    3918b7a3aec0 -> vabc256seq001 (A), add column address
    3918b7a3aec0 -> vabc257seq001 (B) (head), add column address
    <base> -> 3918b7a3aec0 (branchpoint), create account table

    # 查看某个分支的升级历史记录
    $alembic history -r A@head:
    vabc256seq001 -> cd7de7e6dddd (A) (head), test
    3918b7a3aec0 -> vabc256seq001 (A), add column address

    # 也可以查看从基准分支升级上来的历史记录，降级操作也是按照这个顺序降级的
    # 这里的[:]在左边表示从base到A的历史记录，在右边表示 从A开始的历史记录，就像区间一样
    $alembic history -r :A@head
    vabc256seq001 -> cd7de7e6dddd (A) (head), tst
    3918b7a3aec0 -> vabc256seq001 (A), add column address
    <base> -> 3918b7a3aec0 (branchpoint), create account table

    # 当然也可以查看部分历史，不需要全部都列出来
    $alembic history -r :A@head-2
    ```

### 按版本归档

- 数据库升级脚本最好是按照版本进行归档分类

    ```sh
    # 修改 alembic.ini 说明升级脚本路径
    # 指定2.5.6和2.5.7两个版本的升级脚本存放路径
    # %(here)s 表示 alembic.ini 配置文件所在的目录
    version_locations = migration/versions/2.5.6 migration/versions/2.5.7 migration/versions
  
    # 如果版本之间存在相互依赖问题怎么办呢？比如257版本需要往表里新增一个字段，而这个表是在256版本的时候加的，虽说两个版本并行开发，但是难免出现这种情况；
    # 最好是能知道升级顺序，先执行256的脚本，再执行257的脚本（之前考虑过依赖 depends_on 的方案，发现并不合适，因为 depends_on 参数是脚本序号组成的列表，但是并行开发，257 并不知道 256 最后发布的时候序号是多少）;

    # √ 根据实践得出，version_location = v1 v2 v3 这样排序的话，会按照反过来的顺序执行脚本，即：v3、v2、v1


    # 执行命令自动创建2.5.6版本文件夹，并且按照 script.py.mako 模板生成升级脚本
    $alembic revision -m "create post table" --head=base --branch-label=2.5.6 --version-path=migration/versions/2.5.6
  
    # 这样生成的脚本编号仍然是乱序的，虽然可以通过控制台执行 alembic history 来查看升级路径，但是如果想更直观查看，也可以手动修改脚本的命名，比如命名为 "v2.5.16_0001_xxx.py" 第一个下划线前的都作为脚本的序号

    # 后续创建升级脚本的时候，如果指定了分支，会自动放到对应的文件夹下
    $alembic revision -m "add test column" --head=2.5.6
  
    # 会把各个分支下的脚本执行，查看alembic_version可以看到每个版本都有一条记录（这个记录就是head）
    $alembic upgrade heads
  
    # 如果想升级某一个分支呢？
    $alembic upgrade 2.5.6@head
  
    # 如果想单独升级base分支呢？
  
    # 这样就完成了按照版本归档数据库升级脚本，而且不用担心序号重复的问题
    # 为了更直观地看出升级脚本执行顺序（当然也可以通过 alembic history :[branch_name]@head 来查看），也可以自己定义脚本序号比如 v256seq001_test.py
    ```

### 分支合并

- 构造 A B 两个版本基于 `3918b7a3aec0` 同时开发，都创建了 `3918b7a3ae10、3918b7a3ae11` 两个版本文件，而且他们的 `down_revision 和 revision` 值都一样

    ```sh
    A: 3918b7a3aec0 --> 3918b7a3ae10 --> 3918b7a3ae11
    B: 3918b7a3aec0 --> 3918b7a3ae10 --> 3918b7a3ae11
    要求支持 A --> B
    ```

- 尝试使用 `alembic merge` 的方法支持 A 版本升级到 B 版本，实际操作时报错

    ```sh
    # 执行合并
    $alembic merge -m "merge 3918b7a3ae10_add_column_address2 3918b7a3ae10_add_column_address" 3918b7a3ae10 3918b7a3ae10

    # 失败
    FAILED: Duplicate head revisions specified

    # 原因是现在使用的是递增的版本序号，而不是由 alembic 自动生成的，所以序号重复就直接报错了，如果序号不重复倒是可以试试 merge 的方法
    ```

## 添加迁移脚本规范

- 添加指定版本的迁移脚本

    ```sh
    # 指定分支 2.5.6
    $alembic revision -m "script description" --head 2.5.6@head
    # 生成成功
    Generating /admin/tmp/version_control/migration/versions/2.5.6/192b76ee0414_script_description.py ... done
    ```

- 创建一个版本分支

    ```sh
    # 创建版本目录
    cd /path/to/migration/versions
    mkdir 2.5.8
    ```

- 添加版本迁移脚本

    ```sh
    touch v2.5.8seq001_first_script_on_v2_5_8.py

    """first script on v2.5.8

    Revision ID: v2.5.8seq001
    Revises:
    Create Date: 2022-04-13 11:31:23.223368
    
    """
    from alembic import op
    import sqlalchemy as sa
    
    
    # revision identifiers, used by Alembic.
    revision = 'v2.5.8seq001'
    down_revision = None
    branch_labels = ('2.5.8',)      ####### 首个版本需要填写上分支标签
    depends_on = None


    def upgrade():
        pass


    def downgrade():
        pass

    ```

- 升级版本

    ```sh
    $python db_assist.py -t upgrade
    ```

- 降级版本

    ```sh
    # 降级的话，会从 version_num 表里删除一条记录
    # 如果不指明 2.5.6 分支，会默认从 head 分支回退一个版本
    $alembic downgrade 2.5.6@head-1
    ```

# 其他

## `alembic` 基础命令

- `alembic branches` 查看有哪些分支，结果是那些还没有执行应用到数据库中的脚本

- `alembic heads` 查看有哪些分支（查看的是升级脚本的关系，一般只有一个 HEAD，如果使用了多分支，这个表就会出现多条记录）

- `alembic history` 查看升级历史记录

- `alembic upgrade`

    - `alembic upgrade head` 升级到 base 分支的最新版本

    - `alembic upgrade [ver_num]` 执行该升级脚本

    - `alembic upgrade [branch_name@head]` 执行该分支的升级脚本

- `alembic downgrade [version_num]` 降级到版本

    `alembic downgrade -1` 降级到 head 前一版本
