"""Модуль со схемой для вывода баланса."""
from dataclasses import dataclass


@dataclass
class BalanceDTO:
    """."""

    balance: int

    @classmethod
    def from_alchemy(cls, res_balance: int):
        """Метод создания схемы.

        Args:
            res_balance (int): баланс

        Returns:
            BalanceDTO: _description_
        """
        return cls(
            balance=res_balance,
        )
