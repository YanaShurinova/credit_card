"""Базовый модуль."""
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    """."""

    def __init__(self, session: AsyncSession):
        """_summary_.

        Args:
            session (AsyncSession): _description_
        """
        self._session = session
