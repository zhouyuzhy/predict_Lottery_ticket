from lottery.db import Session, session_scope
from lottery.db.model.UnionLotto import UnionLotto


def add_union_lotto(union_lotto):
    with session_scope() as session:
        session.add(union_lotto)


def query_union_lotto_by_period(start_period, end_period):
    with session_scope() as session:
        return session.query(UnionLotto).filter(UnionLotto.periods>=start_period).\
                filter(UnionLotto.periods<=end_period).order_by(UnionLotto.periods).all()
