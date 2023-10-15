"""Таблица запись изменения баланса."""
from sqlalchemy import Column, DateTime, Integer, String

from main_service.src.app.db.models.base import Base


class BalanceLog(Base):
    """_summary_.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = 'balance_log'

    balance_log_id = Column(Integer, primary_key=True)
    card_number = Column(String(100), nullable=False)
    before = Column(Integer, nullable=False)
    after = Column(Integer, nullable=False)
    changes = Column(Integer, nullable=False)
    datetime_utc = Column(DateTime)
