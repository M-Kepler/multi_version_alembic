# -*- coding:utf-8 -*-

from os import path

PROJ_PTH = path.abspath(".")

# ---- 数据库配置

# 配置文件路径
DB_CFG = path.join(PROJ_PTH, "mysql_tools/db.ini")
DB_CFG_SECTION = "DB_Config"

# 初始化脚本
DB_INIT_SQL_FILE = path.join(PROJ_PTH, "mysql_tools/init.sql")

# ---- alembic 配置路径
ALEMBIC_PTH = path.join(PROJ_PTH, "version_control")
ALEMBIC_CFG_PTH = path.join(ALEMBIC_PTH, "alembic.ini")

# alembic version_location 配置
ALEMBIC_CFG_SEC = "alembic"
ALEMBIC_CFG_VER_KEY = "version_locations"

# ---- 数据库迁移脚本路径

VERSION_PTH = path.join(ALEMBIC_PTH, "migration/versions/")
SCRIPT_PTH = path.join(ALEMBIC_PTH, "migration/versions")
