"""Модуль, описывающий классы логов."""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any


@dataclass
class CommonLog:
    """Базовый класс логов."""

    card_number: str
    before: Any
    after: Any
    changes: Any
    _datetime_utc: datetime  # noqa: WPS437

    def __init__(  # noqa: WPS211
        self,
        card_number,
        before,
        after,
        changes,
        date,
    ):
        """
        Инициализация объекта класса.

        Parameters:
            card_number: номер карты,
            before: до изменения,
            after: после изменения,
            changes: изменение,
            date: дата.
        """
        self.card_number = card_number
        self.before = before
        self.after = after
        self.changes = changes
        self._datetime_utc = date


class BalanceLog(CommonLog):
    """Класс, описывающий логи баланса."""

    before: Decimal
    after: Decimal
    changes: Decimal


class LogStorage:
    """Общий класс логов."""

    _balance_logs: dict[str, list[BalanceLog]]
    _other_logs: list[CommonLog]

    def __init__(
        self,
        balance_log: dict[str, list[BalanceLog]] = {},
        other_log: list[CommonLog] = [],
    ):
        """
        Инициализация объекта класса.

        Parameters:
            balance_log: словарь из пар (ключ, list[BalanceLog]),
            other_log: список логов.
        """
        self._balance_logs = balance_log
        self._other_logs = other_log

    def save(self, log: CommonLog):
        """
        Метод сохранения лога.

        Parameters:
            log (CommonLog): лог.
        """
        if isinstance(log, BalanceLog):
            self._balance_logs.update({log.card_number: log})
        else:
            self._other_logs.append(log)

    def get_balance_history(
        self, card_number: str, from_date: datetime, to_date: datetime,
    ) -> list[BalanceLog]:
        """
        Метод получения истории баланса.

        Parameters:
            card_number (str): номер карты,
            from_date (datetime): дата начала истории,
            to_date (datetime): дата конца истории.

        Returns:
            list[BalanceLog]: список BalanceLog.
        """
        user_history = self._balance_logs.get(card_number)
        return list(filter(
            lambda log: from_date <= log._datetime_utc <= to_date,  # noqa: WPS437, E501
            user_history,
        ))
