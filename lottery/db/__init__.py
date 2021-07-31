from sqlalchemy import create_engine, MetaData, Index
from sqlalchemy.engine import reflection
from sqlalchemy.orm import sessionmaker

from lottery import PROJECT_LOTTERY_ABSOLUTE_PATH
from lottery.db.model import Base
from lottery.db.model.UnionLotto import UnionLotto

path = PROJECT_LOTTERY_ABSOLUTE_PATH + "/db/lottery.db"
engine_sqlite = create_engine('sqlite:///' + path)
Session = sessionmaker(bind=engine_sqlite, expire_on_commit=False)
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
    # meta = MetaData()
    # meta.reflect(bind=engine_sqlite)
    # union_lotto_factor = meta.tables['union_lotto_factor']
    # # alternative of retrieving the table from meta:
    # # flows = sqlalchemy.Table('flows', meta, autoload=True, autoload_with=engine)
    #
    # my_index = Index('idx_periods', union_lotto_factor.columns.get('periods'))
    # my_index.create(bind=engine_sqlite)
    #
    # # lets confirm it is there
    # inspector = reflection.Inspector.from_engine(engine_sqlite)
    # print(inspector.get_indexes('union_lotto_factor'))
    Base.metadata.create_all(engine_sqlite, [UnionLotto.__table__], checkfirst=True)
