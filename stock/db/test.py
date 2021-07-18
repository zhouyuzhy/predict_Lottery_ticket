from sqlalchemy.orm import session
from sqlalchemy.sql.functions import now

from stock.db.db_init import session_maker
from stock.db.model.stock_info import StockInfo

stock_info_obj = StockInfo(code="00700", name="腾讯", create_time=now())
with session_maker() as session:
    session.add(stock_info_obj)
