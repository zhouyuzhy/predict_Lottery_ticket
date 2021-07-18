from sqlalchemy import Column, String, DateTime, BigInteger

from stock.db.db_init import Base


class StockInfo(Base):
    __tablename__ = 'plate_stocks'
    id = Column(BigInteger, primary_key=True)
    plate_stock_id = Column(BigInteger, primary_key=True)
    stock_id = Column(BigInteger, primary_key=True)
    create_time = Column(DateTime)
