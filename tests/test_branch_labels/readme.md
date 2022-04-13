- 测试每个版本各自建立一个文件夹存放该版本的升级脚本，各自排序，每个脚本填补上 `branch_labels` 属性表示该脚本属于那个版本的

- 版本分支情况

    ```sh
    A:
        A0001_add_column.py  --  branch_labels = "A" # branch_labels 可以是一个 tuple 或 string
        A0002_add_column.py  --  branch_labels = "A"

    B:
        B0001_add_column.py  --  branch_labels = "B"
        B0002_add_column.py  --  branch_labels = "B"
    ```

- 实施过程

  - 有 `alembic upgrade [branch_name]@head` 命令

    坑的是，这个 `branch_label` 和 `revision` 一样，是用来表示一个版本号的，并不是想象中的那样，属于A版本的升级脚本就加上这个属性，然后升级的时候 `alembic upgrade A@head`

    就可以一次执行完成全部A版本的升级脚本了...

  - 报错 `FAILED: Branch name 'A' in revision vabc256seq002 already used by revision vabc256seq001`

- 当存在两个升级脚本，他们的 `down_revision` 一样，版本好不一样的时候，可以通过 `branch_labels` 标签来区分，并且可以通过 `alembic upgrade [branch_name]@head` 命令来进行升级

- 如果分支版本中添加了 `branch_labels` 的话，想新建升级脚本就要指定分支，否则无法新建

    ```sh
    # 一个脚本中声明了 branch_labels
    $alembic revision -m "test"
    # 报错
    FAILED: Multiple heads are present; please specify the head revision on which the new revision should be based, or perform a merge.

    # 生成时指定分支
    $alembic revision -m "test" --head A@head

    $alembic history
    # 虽然查看生成的脚本中 branch_labels 还是None，但是通过命令来看可以追溯到它所在的分支
    vabc256seq001 -> cd7de7e6dddd (A) (head), tst
    3918b7a3aec0 -> vabc256seq001 (A), add column address
    3918b7a3aec0 -> vabc257seq001 (B) (head), add column address
    <base> -> 3918b7a3aec0 (branchpoint), create account table

    # 查看某个分支的升级历史记录
    $alembic history -r A:  # 注意这里有个冒号
    vabc256seq001 -> cd7de7e6dddd (A) (head), tst
    3918b7a3aec0 -> vabc256seq001 (A), add column address

    # 也可以查看从基准分支升级上来的历史记录，降级操作也是按照这个顺序降级的
    $alembic history -r :A@head
    vabc256seq001 -> cd7de7e6dddd (A) (head), tst
    3918b7a3aec0 -> vabc256seq001 (A), add column address
    <base> -> 3918b7a3aec0 (branchpoint), create account table

    # 当然也可以查看部分历史，不需要全部都列出来
    $alembic history -r :A@head-2
    ```
