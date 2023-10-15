"""Модуль для хранения класса Токен."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Token:
    """Класс-Токен."""

    card_number: str
    token: str
    expires: datetime

    def __init__(self, card_number: str, token: str, expires: datetime):
        """Инициализация.

        Parameters:
            card_number (str): номер карты
            token (str): токен
            expires (datetime): истекает
        """
        self.card_number = card_number
        self.token = token
        self.expires = expires
