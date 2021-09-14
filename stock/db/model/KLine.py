from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, BigInteger

from stock.db.model import Base


class KLine(Base):
    __tablename__ = 'kline'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(100))
    time_key = Column(DateTime())
    kline_level = Column(String(100))
    open = Column(DECIMAL(20,2))
    close = Column(DECIMAL(20,2))
    high = Column(DECIMAL(20,2))
    low = Column(DECIMAL(20,2))
    pe_ratio = Column(DECIMAL(20,2))
    turnover_rate = Column(DECIMAL(20,2))
    volume = Column(DECIMAL(20,2))
    turnover = Column(DECIMAL(20,2))
    change_rate = Column(DECIMAL(20,2))
    last_close = Column(DECIMAL(20,2))
    create_time = Column(DateTime())
