# -*- coding:utf-8 -*-

"""
数据表模型
"""

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TableStudent(Base):
    __tablename__ = 'student'

    id = Column(String(9), nullable=False, index=True, primary_key=True)
    name = Column(String(64), nullable=False)
    description = Column(String(128), nullable=False)
