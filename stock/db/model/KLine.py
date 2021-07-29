from sqlalchemy import Column, Integer, String, DateTime, DECIMAL

from stock.db.model import Base


class KLine(Base):
    __tablename__ = 'kline'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(100))
    time_key = Column(DateTime())
    open = Column(DECIMAL())
    close = Column(DECIMAL())
    high = Column(DECIMAL())
    low = Column(DECIMAL())
    pe_ratio = Column(DECIMAL())
    turnover_rate = Column(DECIMAL())
    volume = Column(Integer())
    turnover = Column(DECIMAL())
    change_rate = Column(DECIMAL())
    last_close = Column(DECIMAL())