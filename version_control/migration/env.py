# -*- coding:utf-8 -*-

from logging.config import fileConfig

from alembic import context
from mysql_tools.config import DB_Config
from mysql_tools.modules import Base
from sqlalchemy import engine_from_config, pool

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


# 配置连接信息

# 只修改了保存在内存里的信息，没有真正修改配置文件
cfg_tool = DB_Config()
config.set_main_option(
    name='sqlalchemy.url',
    value="mysql+pymysql://{user}:{pwd}@{host}:{port}/{db_name}".format(
        user=cfg_tool.db_user,
        pwd=cfg_tool.db_pwd,
        host=cfg_tool.db_host,
        port=cfg_tool.db_port,
        db_name=cfg_tool.db_name
    )
)

# alembic/config.py/main 的时候就已经设置好Config了
# 执行命令前就初始化了script/base.py/ScriptDirectory/version_ocations，所以无法像修改 sqlalchemy.url那样运行时指定数据库链接
# alembic/command.py/upgrade 的时候就已经设置好script来自文件了
# 这个env.py是在 base.py/run_env 函数的时候加载进来进行执行
# 涉及好几个上下文，首先是环境上下文 runtime/environment.py/EnvironmentContext
# 还有执行升级操作的上下文 runtime/migration.py/MigrationContext

# 配置版本文件夹
# 解析alembic.ini时， %(hear)s 会被替换成配置文件所在路径加入到config中

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
