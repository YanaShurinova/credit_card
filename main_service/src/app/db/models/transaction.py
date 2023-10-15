"""Таблица транзакций."""
from sqlalchemy import Column, Integer, String

from main_service.src.app.db.models.base import Base


class Transaction(Base):
    """_summary_.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = 'transaction'

    transaction_id = Column(Integer, primary_key=True)
    log_storage_id = Column(Integer, nullable=False)
    user_storage_id = Column(String(100), nullable=False)
