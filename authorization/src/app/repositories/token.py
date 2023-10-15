"""Модуль для работы с токеном."""
import random
import string
from datetime import datetime, timedelta

from sqlalchemy import insert, select

from authorization.src.app.db.models.token import Token
from authorization.src.app.dto.token import TokenDTO
from authorization.src.app.repositories.base import BaseRepository


def get_random_string(length: int):
    """Метод получения случайной строки.

    Parameters:
        length (int): длина

    Returns:
        str: строка
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for letter in range(length))  # noqa: S311, E501


class TokenRepository(BaseRepository):
    """."""

    async def create_token(self, user_id):
        """Метод создания токена.

        Args:
            user_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        await self._session.execute(
            insert(Token).values(
                user_id=user_id,
                token=get_random_string(10),
                expires=datetime.now() + timedelta(weeks=1),
            ),
        )
        record = (await self._session.execute(
            select(Token).where(Token.user_id == user_id),
        )).scalar()
        return TokenDTO.from_alchemy(record)

    async def get_by_id(self, user_id):
        """_summary_.

        Args:
            user_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        record = (await self._session.execute(
            select(Token).where(
                Token.user_id == user_id and Token.expires > datetime.now(),
            ),
        )).scalar()
        return TokenDTO.from_alchemy(record)
