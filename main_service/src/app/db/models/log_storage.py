"""Таблица хранилища записей."""
from sqlalchemy import Column, Integer, String

from main_service.src.app.db.models.base import Base


class LogStorage(Base):
    """_summary_.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = 'log_storage'

    log_storage_id = Column(Integer, primary_key=True)
    balance_log_id = Column(String(100), nullable=False)
    common_log_id = Column(String(100), nullable=False)
