from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from stock.db.model import Base
from stock.db.model.KLine import KLine
from stock.db.model.StockInfo import StockInfo

engine_sqlite = create_engine('sqlite:///stock.db')
Session = sessionmaker(bind=engine_sqlite)

if __name__ == '__main__':
    Base.metadata.create_all(engine_sqlite,[KLine.__table__, StockInfo.__table__], checkfirst=True)
