"""Модуль, описывающий работу с клиентом."""
from datetime import datetime
from decimal import Decimal

from src.dto.models.log import BalanceLog, CommonLog, LogStorage
from src.dto.models.user_storage import UserStorage


class Transactions:  # noqa: WPS214
    """Класс, описывающий методы работы с клиентом."""

    _user_storage: UserStorage
    _history: LogStorage

    def __init__(  # noqa: N802
        self,
        storage=None,  # noqa: B008
        history=None,  # noqa: B008
    ):
        """Конструктор.

        Parameters:
            storage (UserStorage): хранилище пользователей.
            history (LogStorage): хранилище логов.
        """
        self._user_storage = storage if storage is not None else UserStorage()
        self._history = history if history is not None else LogStorage()

    def get_balance(self, card_number: str):
        """Получение баланса.

        Parameters:
            card_number (str): номер карты

        Returns:
            Decimal: баланс.
        """
        user = self._user_storage.get_user(card_number)
        if user:
            return user.balance

    def withdrawal(self, card_number: str, amount: Decimal):
        """Метод списания.

        Parameters:
            card_number (str): номер карты.
            amount (Decimal): сумма списания.
        """
        if self._user_storage.get_user(card_number):
            self._check_amount(amount)
            self._change_balance(card_number, -amount)

    def deposit(self, card_number: str, amount: Decimal):
        """Метод зачисления.

        Parameters:
            card_number (str): номер карты.
            amount (Decimal): сумма зачисления.
        """
        if self._user_storage.get_user(card_number):
            self._check_amount(amount)
            self._change_balance(card_number, amount)

    def update_info(self, card_number: str, new_info: dict):
        """Метод обновления информации о пользователе.

        Parameters:
            card_number (str): номер карты.
            new_info (dict): новая информация.
        """
        user = self._user_storage.get_user(card_number)
        if user:
            information = {**user.info, **new_info}
            self._history.save(CommonLog(
                card_number=card_number,
                before=user.info,
                after=information,
                changes=new_info,
                date=datetime.now(),
            ))
            user.info = information

    def change_limit(self, card_number: str, new_limit: Decimal):
        """Метод изменения лимита.

        Parameters:
            card_number (str): номер карты.
            new_limit (Decimal): новый лимит.

        Raises:
            ValueError: Новый лимит меньше предыдущего.
        """
        user = self._user_storage.get_user(card_number)
        if user:
            if new_limit > user.limit:
                self._history.save(CommonLog(
                    card_number=card_number,
                    before=user.limit,
                    after=new_limit,
                    changes=new_limit,
                    date=datetime.now(),
                ))
                user.limit = new_limit
            else:
                raise ValueError('Новый лимит меньше предыдущего.')

    def get_history(  # noqa: WPS615
        self,
        card_number: str,
        data_from,
        data_to,
    ):
        """Метод получения истории.

        Parameters:
            card_number (str): номер карты
            data_from (datetime): дата начала
            data_to (datetime): дата конца

        Returns:
            LogStorage: историю
        """
        if self._user_storage.get_user(card_number):
            return self._history.get_balance_history(
                card_number,
                data_from,
                data_to,
            )

    def _change_balance(self, card_number: str, amount: Decimal):
        """Метод изменения баланса.

        Parameters:
            card_number (str): номер карты.
            amount (Decimal): сумма изменения.
        """
        user = self._user_storage.get_user(card_number)
        self._history.save(BalanceLog(
            card_number=card_number,
            before=user.balance,
            after=user.balance + amount,
            changes=amount,
            date=datetime.now(),
        ))
        user.balance = user.balance + amount

    def _check_amount(self, amount: Decimal):
        """Метод проверки суммы.

        Parameters:
            amount (Decimal): сумма.

        Raises:
            ValueError: Данного пользователя не существует.

        Returns:
            bool: проверка на положительность
        """
        if amount > 0:
            return True
        raise ValueError('Зачисление/списание только для величин > 0')
