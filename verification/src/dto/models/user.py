"""Модуль, описывающий датакласс - клиент."""
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class User:
    """Датакласс клиента."""

    card_number: str
    limit: Decimal
    info: dict  # noqa: WPS110
    _balance: Decimal

    @property
    def balance(self):
        """Описание property.

        Returns:
            Decimal: баланс
        """
        return self._balance

    @balance.setter
    def balance(self, new_balance):
        if new_balance < self.limit < 0:
            raise ValueError('Баланс отрицательный')
        self._balance = new_balance
