from sqlalchemy import Column, String, DateTime, BigInteger, DECIMAL

from stock.db.db_init import Base


class StockRelative(Base):
    __tablename__ = 'stock_relative'
    id = Column(BigInteger, primary_key=True)
    stock_info_id_from = Column(BigInteger)
    stock_info_id_to = Column(BigInteger)
    relative_strong = Column(DECIMAL(10, 2))
    key_time = Column(DateTime)
    create_time = Column(DateTime)
