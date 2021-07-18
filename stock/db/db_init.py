from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

#创建引擎
engine = create_engine("mysql+pymysql://stock:123456@127.0.0.1:3306/stock", max_overflow=5)
session = Session(engine)

Base = declarative_base()

@contextmanager
def session_maker(session=session):
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
