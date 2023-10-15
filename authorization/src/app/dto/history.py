"""Модуль для схемы записи истории."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class HistoryDTO:
    """."""

    before: int
    after: int
    changes: int
    datetime_utc: datetime

    @classmethod
    def from_alchemy(cls, record):
        """Метод создания схемы.

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
