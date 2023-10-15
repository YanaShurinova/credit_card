"""Модуль, описывающий хранилище клиента."""
from src.dto.models.user import User


class UserStorage:
    """Класс, описывающий хранилище клиентов."""

    _active: dict[str, User]
    _closed: list[str, User]

    def __init__(self, active=None, closed=None):
        """Инициализация объекта класса.

        Parameters:
            active: словарь активных пользователей.
            closed: список закрытых пользователей.
        """
        self._active = active if active is not None else {}
        self._closed = closed if closed is not None else {}

    def add(self, card_number: str, info: dict):  # noqa: WPS110
        """Метод добавления пользователя.

        Parameters:
            card_number (str): номер карты.
            info (dict): информация о пользователе.

        Raises:
            ValueError: Данный номер карты занят.
        """
        closed_keys = [user[0] for user in self._closed]
        if card_number in self._active.keys() and card_number in closed_keys:
            raise ValueError('Данный номер карты занят.')
        if card_number in self._active.keys():
            self._closed.append([card_number, User(
                card_number=card_number,
                limit=0,
                info=info,
                _balance=0,
            )])
        else:
            self._active.update({card_number: User(
                card_number=card_number,
                limit=0,
                _balance=0,
                info=info,
            )})

    def get_user(self, card_number: str) -> User:
        """Метод получения пользователя.

        Parameters:
            card_number (str): номер карты.

        Raises:
            ValueError: Данный номер карты не существует.

        Returns:
            User: пользователь.
        """
        if self._active.get(card_number):
            return self._active.get(card_number)
        raise ValueError('Данного пользователя не существует.')

    def update_user(self, user: User):
        """Метод обновления пользователя.

        Parameters:
            user (User): сам пользователь.
        """
        old_user = self.get_user(user.card_number)
        if old_user:
            old_user.balance = user.balance
            old_user.info = user.info
            old_user.limit = user.limit

    def close(self, card_number: str):
        """Метод закрытия клиента/добавления в закрытые.

        Parameters:
            card_number (str): номер карты
        """
        user = self.get_user(card_number)
        if user:
            self._active.pop(card_number)
            self._closed.append([card_number, user])
