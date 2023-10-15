"""Таблица пользователя."""
from sqlalchemy import Column, Integer, String

from main_service.src.app.db.models.base import Base


class User(Base):
    """_summary_.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = 'user'

    card_number = Column(String(100), primary_key=True)
    balance = Column(Integer, nullable=False)
    card_limit = Column(Integer, nullable=False)
    name = Column(String(50), nullable=False)  # noqa: WPS432
    age = Column(Integer, nullable=False)
