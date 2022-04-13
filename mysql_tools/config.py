# -*- coding: utf-8 -*-

"""
数据库连接配置
"""
from const import DB_CFG, DB_CFG_SECTION
from ConfigParser import ConfigParser


class DB_Config(object):
    _CFG = ConfigParser()
    _CFG.read(DB_CFG)

    @property
    def db_host(self):
        return self._CFG.get(DB_CFG_SECTION, "database_host")

    @property
    def db_port(self):
        return self._CFG.get(DB_CFG_SECTION, "database_port")

    @property
    def db_name(self):
        return self._CFG.get(DB_CFG_SECTION, "database_name")

    @property
    def db_user(self):
        return self._CFG.get(DB_CFG_SECTION, "database_username")

    @property
    def db_pwd(self):
        return self._CFG.get(DB_CFG_SECTION, "database_password")
