"""Модуль для схем."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BalanceDTO:
    """Схема для запроса баланса.

    Returns:
        _type_: _description_
    """

    balance: int

    @classmethod
    def from_alchemy(cls, res_balance):
        """_summary_.

        Args:
            res_balance (_type_): _description_

        Returns:
            _type_: _description_
        """
        return cls(
            balance=res_balance,
        )


@dataclass
class HistoryDTO:
    """Схема для запроса истории баланса.

    Returns:
        _type_: _description_
    """

    before: int
    after: int
    changes: int
    datetime_utc: datetime

    @classmethod
    def from_alchemy(cls, record):
        """_summary_.

        Args:
            record (_type_): _description_

        Returns:
            _type_: _description_
        """
        return cls(
            before=record.before,
            after=record.after,
            changes=record.changes,
            datetime_utc=record.datetime_utc,
        )
