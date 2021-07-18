from sqlalchemy import Column, String, DateTime, BigInteger

from stock.db.db_init import Base


class StockInfo(Base):
    __tablename__ = 'stock_info'
    id = Column(BigInteger, primary_key=True)
    code = Column(String(255))
    name = Column(String(255))
    create_time = Column(DateTime)
