from sqlalchemy import Column, String, DateTime, BigInteger, DECIMAL

from stock.db.db_init import Base


class StockPrice(Base):
    __tablename__ = 'stock_price'
    id = Column(BigInteger, primary_key=True)
    stock_info_id = Column(BigInteger)
    time_key = Column(DateTime)
    open_price = Column(DECIMAL(10, 2))
    close_price = Column(DECIMAL(10, 2))
    high_price = Column(DECIMAL(10, 2))
    low_price = Column(DECIMAL(10, 2))
    pe_ratio = Column(DECIMAL(10, 2))
    turnover_rate = Column(DECIMAL(10, 2))
    volume = Column(BigInteger)
    turnover = Column(DECIMAL(10, 2))
    change_rate = Column(DECIMAL(10, 2))
    create_time = Column(DateTime)
