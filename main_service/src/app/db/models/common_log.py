"""Таблица записей изменений не баланса."""
from sqlalchemy import Column, DateTime, Integer, String

from main_service.src.app.db.models.base import Base


class CommonLog(Base):
    """_summary_.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = 'common_log'

    common_log_id = Column(Integer, primary_key=True)
    card_number = Column(String(100))
    before = Column(String, nullable=False)
    after = Column(String, nullable=False)
    changes = Column(String, nullable=False)
    datetime_utc = Column(DateTime)
