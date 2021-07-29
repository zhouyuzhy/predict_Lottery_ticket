from sqlalchemy import Column, Integer, String, DateTime, DECIMAL

from stock.db.model import Base


class StockInfo(Base):
    __tablename__ = 'stock_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(100))
    name = Column(String(100))
    stock_type = Column(String(100))