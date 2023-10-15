"""Модуль для схемы пользователя."""
from dataclasses import dataclass

from authorization.src.app.db.models.user import User


@dataclass
class UserDTO:
    """."""

    user_id: str
    login: str
    password: str

    @classmethod
    def from_alchemy(cls, record: User):
        """_summary_.

        Args:
            record (User): _description_

        Returns:
            _type_: _description_
        """
        return cls(
            user_id=record.user_id,
            login=record.login,
            password=record.password,
        )
