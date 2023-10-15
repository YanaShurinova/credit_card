"""Таблица банковского пользователя."""
from sqlalchemy import Column, Integer, String

from authorization.src.app.db.models.base import Base


class User(Base):
    """Таблица пользователя."""

    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    login = Column(String(50), nullable=False)  # noqa: WPS432
    password = Column(String(50), nullable=False)  # noqa: WPS432
