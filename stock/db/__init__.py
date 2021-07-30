from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from stock import PROJECT_STOCK_ABSOLUTE_PATH
from stock.db.model import Base
from stock.db.model.KLine import KLine
from stock.db.model.StockInfo import StockInfo

path = PROJECT_STOCK_ABSOLUTE_PATH + "/db/stock.db"
engine_sqlite = create_engine('sqlite:///'+path)
Session = sessionmaker(bind=engine_sqlite,expire_on_commit=False)
from contextlib import contextmanager


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == '__main__':
    Base.metadata.create_all(engine_sqlite,[KLine.__table__, StockInfo.__table__], checkfirst=True)
