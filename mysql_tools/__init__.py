# -*- coding: utf-8 -*-

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import DB_Config


def _get_conn_str():
    """
    获取数据库连接串
    """
    cfg_tool = DB_Config()
    conn_str = (
        'mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}?charset=utf8'.format(
            user=cfg_tool.db_user,
            pwd=cfg_tool.db_pwd,
            host=cfg_tool.db_host,
            port=cfg_tool.db_port,
            db=cfg_tool.db_name
        ))
    return conn_str


engine = create_engine(_get_conn_str(), pool_size=100,
                       max_overflow=500, pool_recycle=3600)

DBSession = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = DBSession()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
