from datetime import datetime

from stock.db import Session, KLine, session_scope
from stock.db.model import KLineLevel


def add_kline(kLine):
    # 创建Session类实例
    with session_scope() as session:
        kLine.create_time = datetime.now()
        session.add(kLine)


def query_single_kline(code, time_key, kline_level=KLineLevel.K_DAY):
    with session_scope() as session:
        return session.query(KLine).filter_by(code=code) \
            .filter(KLine.kline_level == kline_level) \
        .filter(KLine.time_key == time_key).first()


def query_kline(code, beginTime=None, endTime=None, kline_level=KLineLevel.K_DAY):
    with session_scope() as session:
        return session.query(KLine).filter_by(code=code)\
            .filter(KLine.time_key>=beginTime)\
            .filter(KLine.time_key<=endTime)\
            .filter(KLine.kline_level==kline_level)\
            .order_by(KLine.time_key).all()


def delete_kline(kLine):
    with session_scope() as session:
        session.delete(kLine)