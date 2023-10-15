"""Модуль для работы с транзакцией."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import insert, select, update

from main_service.src.app.db.models.balance_log import BalanceLog
from main_service.src.app.db.models.common_log import CommonLog
from main_service.src.app.db.models.log_storage import LogStorage
from main_service.src.app.db.models.transaction import Transaction
from main_service.src.app.db.models.user import User
from main_service.src.app.db.models.user_storage import UserStorage
from main_service.src.app.dto.transaction import BalanceDTO, HistoryDTO
from main_service.src.app.repositories.base import BaseRepository


class TransactionRepository(BaseRepository):
    """Класс транзакции.

    Args:
        BaseRepository (_type_): _description_
    """

    async def get_balance(self, card_number: str):
        """Метод получения баланса.

        Args:
            card_number (str): _description_

        Returns:
            BalanceDTO: _description_
        """
        balance = (await self._session.execute(
            select(User.balance).
            select_from(Transaction).
            outerjoin(
                UserStorage,
                Transaction.user_storage_id == UserStorage.user_card_number,
            ).
            outerjoin(User, UserStorage.user_card_number == User.card_number).
            where(
                User.card_number == card_number,  # noqa: WPS204
            ),
        )).scalar()
        return BalanceDTO.from_alchemy(balance)

    async def get_balance_history(self, card_number: str, data_from, data_to):
        """Метод получения истории баланса.

        Args:
            card_number (str): _description_
            data_from (_type_): _description_
            data_to (_type_): _description_

        Returns:
            _type_: _description_
        """
        record = (await self._session.execute(
            select(BalanceLog).
            select_from(Transaction).
            outerjoin(
                LogStorage,
                Transaction.log_storage_id == LogStorage.log_storage_id,
            ).
            outerjoin(
                BalanceLog,
                LogStorage.balance_log_id == BalanceLog.card_number,
            ).
            where(
                BalanceLog.card_number == card_number and data_from < BalanceLog.datetime_utc < data_to,  # noqa: E501
            ),
        )).scalar()
        return HistoryDTO.from_alchemy(record)

    async def withdrawal(self, card_number: str, amount: Decimal):
        """Метод списания.

        Args:
            card_number (str): _description_
            amount (Decimal): _description_

        Returns:
            _type_: _description_
        """
        user = (await self._session.execute(
            select(User).
            select_from(Transaction).
            outerjoin(
                UserStorage,
                Transaction.user_storage_id == UserStorage.user_card_number,
            ).
            outerjoin(User, UserStorage.user_card_number == User.card_number).
            where(User.card_number == card_number),
        )).scalar()
        if user:
            self._check_amount(amount)
            self._change_balance(card_number, -amount)
            return 200  # noqa: WPS432

    async def deposit(self, card_number: str, amount: Decimal):
        """Метод зачисления.

        Args:
            card_number (str): _description_
            amount (Decimal): _description_

        Returns:
            _type_: _description_
        """
        user = (await self._session.execute(
            select(User).
            select_from(Transaction).
            outerjoin(
                UserStorage,
                Transaction.user_storage_id == UserStorage.user_card_number,
            ).
            outerjoin(User, UserStorage.user_card_number == User.card_number).
            where(User.card_number == card_number),
        )).scalar()
        if user:
            self._check_amount(amount)
            self._change_balance(card_number, amount)
            return 200  # noqa: WPS432

    async def change_limit(self, card_number: str, new_limit: Decimal):
        """Метод изменения лимита.

        Parameters:
            card_number (str): номер карты.
            new_limit (Decimal): новый лимит.

        Raises:
            ValueError: Новый лимит меньше предыдущего.

        Returns:
            _type_: _description_
        """
        user = (await self._session.execute(
            select(User).
            select_from(Transaction).
            outerjoin(
                UserStorage,
                Transaction.user_storage_id == UserStorage.user_card_number,
            ).
            outerjoin(User, UserStorage.user_card_number == User.card_number).
            where(User.card_number == card_number),
        )).scalar()
        if user:
            if new_limit > user.card_limit:
                await self._session.execute(
                    insert(CommonLog).
                    values(
                        card_number=user.card_number,
                        before=str(user.card_limit),
                        after=str(new_limit),
                        changes=str(new_limit),
                        datetime_utc=datetime.now(),
                    ),
                )
                await self._session.execute(
                    update(User).
                    where(User.card_number == card_number).
                    values(card_limit=new_limit),
                )
                return (await self._session.execute(
                    select(User).
                    select_from(Transaction).
                    outerjoin(
                        UserStorage,
                        Transaction.user_storage_id == UserStorage.user_card_number,  # noqa: E501
                    ).
                    outerjoin(
                        User,
                        UserStorage.user_card_number == User.card_number,
                    ).
                    where(User.card_number == card_number),
                )).scalar()
            raise ValueError('Новый лимит меньше предыдущего.')

    async def _change_balance(self, card_number: str, amount: Decimal):
        """Метод изменения баланса.

        Parameters:
            card_number (str): номер карты.
            amount (Decimal): сумма изменения.
        """
        user = (await self._session.execute(
            select(User).
            select_from(Transaction).
            outerjoin(
                UserStorage,
                Transaction.user_storage_id == UserStorage.user_card_number,
            ).
            outerjoin(User, UserStorage.user_card_number == User.card_number).
            where(User.card_number == card_number),
        )).scalar()

        await self._session.execute(
            insert(BalanceLog).
            values(
                card_number=card_number,
                before=user.balance,
                after=user.balance + amount,
                changes=amount,
                datetime_utc=datetime.now(),
            ),
        )
        await self._session.execute(
            update(User).where(
                User.card_number == card_number,
            ).values(balance=User.balance + amount),
        )

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
