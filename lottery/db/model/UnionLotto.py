from sqlalchemy import Column, Integer, String, DateTime, DECIMAL

from lottery.db import Base


class UnionLotto(Base):
    __tablename__ = 'union_lotto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    periods = Column(Integer)
    red_ball_1 = Column(Integer)
    red_ball_2 = Column(Integer)
    red_ball_3 = Column(Integer)
    red_ball_4 = Column(Integer)
    red_ball_5 = Column(Integer)
    red_ball_6 = Column(Integer)
    blue_ball = Column(Integer)
    jackpot = Column(DECIMAL(20,2))
    first_prize_count = Column(Integer)
    first_prize_money = Column(DECIMAL(20,2))
    second_prize_count = Column(Integer)
    second_prize_money = Column(DECIMAL(20, 2))
    buy_money = Column(DECIMAL(20, 2))
    show_time = Column(DateTime())
