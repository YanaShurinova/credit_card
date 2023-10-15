"""Модуль для схемы токена."""
from dataclasses import dataclass
from datetime import datetime

from authorization.src.app.db.models.token import Token


@dataclass
class TokenDTO:
    """."""

    user_id: int
    token: str
    expires: datetime

    @classmethod
    def from_alchemy(cls, record: Token):
        """Метод создания схемы.

        Args:
            record (Token): _description_

        Returns:
            _type_: _description_
        """
        return cls(
            user_id=record.user_id,
            token=record.token,
            expires=record.expires,
        )
