from stock.db import Session, KLine


def add_kline(kLine):
    # 创建Session类实例
    session = Session()
    session.add(kLine)
    session.commit()
    
    
def query_kline(code, beginTime=None, endTime=None):
    session = Session()
    return session.query(KLine).filter_by(code=code).\
        filter(KLine.time_key>=beginTime).\
        filter(KLine.time_key<=endTime).all()
