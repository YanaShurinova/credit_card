"""Модуль для хранения pydantic моделей."""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class TokenBase(BaseModel):
    """Модель токена."""

    token: str
    expires: datetime
    token_type: Optional[str] = 'bearer'

    class Config:
        """Класс конфигураций."""

        allow_population_by_field_name = True
        orm_mode = True


class Balance(BaseModel):
    """."""

    balance: int

    class Config:
        """."""

        orm_mode = True


class ChangeBalance(BaseModel):
    """."""

    card_number: str
    amount: int


class BalanceLog(BaseModel):
    """."""

    card_number: str
    before: Decimal
    after: Decimal
    changes: Decimal
    _datetime_utc: datetime
