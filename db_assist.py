# -*- coding: utf-8 -*-

import pdb
import subprocess
import os

import argparse
import alembic.config
from sqlalchemy.exc import OperationalError

from mysql_tools import engine
from mysql_tools.config import DB_Config
from configparser import ConfigParser
import const


class DBHelper(object):
    def __init__(self, is_confirmed=False):
        self.cfg_tool = DB_Config()
        self.db_user = self.cfg_tool.db_user
        self.db_pwd = self.cfg_tool.db_pwd
        self.db_name = self.cfg_tool.db_name
        self.is_confirmed = is_confirmed

    @staticmethod
    def _is_db_existed():
        """
        检查数据库是否已经存在
        """
        try:
            conn = engine.connect()
            conn.connect()
            return True
        except OperationalError:
            return False

    def _init_db_structure(self):
        """
        初始化数据库结构
        """
        if not self.is_confirmed:
            is_existed = self._is_db_existed()
            if is_existed:
                print("Warning: database already exists, this action will erase all data!")
                choice = input('Continue init database? (y/n): ')
                if choice.lower() != 'y':
                    print("Mission abort!")
                    return False
        cmd1 = ("mysql -u%s -p%s -e 'drop database if exists %s'" %
                (self.db_user, self.db_pwd, self.db_name))

        # 导入数据库初始化脚本
        cmd2 = "mysql -u%s -p%s < %s" % (self.db_user, self.db_pwd,
                                         const.DB_INIT_SQL_FILE)

        for cmd in [cmd1, cmd2]:
            retcode = subprocess.call(cmd, shell=True)
            if retcode != 0:
                raise Exception("run cmd: %s error" % cmd)
        return True

    def _upgrade(self):
        """
        执行 alembic upgrade 命令开始数据库迁移

        注意！要进入到 alembic.ini 所在路径执行 alembic 命令
        """
        self._init_alembic_cfg()
        os.chdir(const.ALEMBIC_PTH)
        alembic.config.main(argv=['--raiseerr', 'upgrade', 'heads'])

    def _get_version_locations(self):
        """
        遍历 migration/version 下的版本文件夹，组装成版本链
        """
        exclude_dirs = ['__pycache__', 'test']

        migrate_script_path = []
        version_dirs = []

        # 各个版本的迁移脚本
        for _, dirs, _ in os.walk(const.VERSION_PTH, topdown=False):
            for item in dirs:
                if item not in exclude_dirs:
                    version_dirs.append(const.VERSION_PTH+ "/" + item)

        # 注意这里要按版本大小倒序
        # 比如版本目录为：['2.5.6', '2.5.7', '2.5.8']，那么迁移时是倒序执行的
        migrate_script_path.extend(sorted(version_dirs, reverse=True))

        # 各个版本外的迁移脚本（比如一些初始化脚本）
        migrate_script_path.append(const.VERSION_PTH)
        return ' '.join(migrate_script_path)

    def _init_alembic_cfg(self):
        """
        修改 alembic.ini 的 version_locations 配置
        以支持多版本
        """
        cfg_api = ConfigParser()
        cfg_api.read(const.ALEMBIC_CFG_PTH)
        cfg_api.set(const.ALEMBIC_CFG_SEC, const.ALEMBIC_CFG_VER_KEY,
                    self._get_version_locations())
        with open(const.ALEMBIC_CFG_PTH, "w") as fd:
            cfg_api.write(fd)

    def do_init(self):
        """
        清除数据库，重新初始化
        """
        if self._init_db_structure():
            self._upgrade()

    def do_upgrade(self):
        """
        执行升级脚本
        """
        is_existed = self._is_db_existed()
        if not is_existed:
            raise Exception("Database not exist")
        self._upgrade()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", "--type",
        type=str,
        choices=["init", "upgrade", "help"],
        default="help",
        help="operation type"
    )
    parser.add_argument(
        "-y",
        help="do it, without any warning",
        action="store_true"
    )

    args = parser.parse_args()

    is_confirmed = False
    if args.y:
        is_confirmed = True

    if args.type == "init":
        DBHelper(is_confirmed=is_confirmed).do_init()
    elif args.type == "upgrade":
        DBHelper(is_confirmed=is_confirmed).do_upgrade()
    else:
        print("-h for usage")


if __name__ == "__main__":
    main()
    # DBHelper().do_upgrade()
