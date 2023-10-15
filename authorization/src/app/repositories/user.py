"""Модуль для работы с банковским работником."""
from sqlalchemy import select

from authorization.src.app.db.models.user import User
from authorization.src.app.dto.user import UserDTO
from authorization.src.app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """."""

    async def get_user(self, login: str, password: str):
        """_summary_.

        Args:
            login (str): _description_
            password (str): _description_

        Returns:
            _type_: _description_
        """
        record = (await self._session.execute(
            select(User).where(
                User.login == login and User.password == password,
            ),
        )).scalar()
        return UserDTO.from_alchemy(record)
