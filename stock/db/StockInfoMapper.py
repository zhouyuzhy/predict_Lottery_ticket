from stock.db import Session, StockInfo


def add_stock_info(stockInfo):
    # 创建Session类实例
    session = Session()
    session.add(stockInfo)
    session.commit()


def query_stock_info(code):
    session = Session()
    return session.query(StockInfo).filter_by(code=code).all()
