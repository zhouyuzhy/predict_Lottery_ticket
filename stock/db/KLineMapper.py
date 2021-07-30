from stock.db import Session, KLine, session_scope


def add_kline(kLine):
    # 创建Session类实例
    session = Session()
    session.add(kLine)
    session.commit()
    

def query_single_kline(code, time_key):
    with session_scope() as session:
        return session.query(KLine).filter_by(code=code). \
            filter(KLine.time_key == time_key).first()


def query_kline(code, beginTime=None, endTime=None):
    with session_scope() as session:
        return session.query(KLine).filter_by(code=code).\
            filter(KLine.time_key>=beginTime).\
            filter(KLine.time_key<=endTime).order_by(KLine.time_key).all()
