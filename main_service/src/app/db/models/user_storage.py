"""Таблица для хранилища юзеров."""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from main_service.src.app.db.models.base import Base


class UserStorage(Base):
    """_summary_.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = 'user_storage'

    user_storage_id = Column(Integer, primary_key=True)
    user_card_number = Column(String(100), ForeignKey('user.card_number'))
    is_active = Column(Boolean, server_default='f')
