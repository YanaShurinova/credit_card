"""Таблица токен."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from authorization.src.app.db.models.base import Base


class Token(Base):
    """Таблица токен."""

    __tablename__ = 'token'

    token_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    token = Column(String(100))
    expires = Column(DateTime())
