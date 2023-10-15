from datetime import datetime

import pytest
import pytest_asyncio
from sqlalchemy import insert

from main_service.src.app.db.models.balance_log import BalanceLog
from main_service.src.app.db.models.log_storage import LogStorage
from main_service.src.app.db.models.transaction import Transaction
from main_service.src.app.db.models.user import User
from main_service.src.app.db.models.user_storage import UserStorage
from main_service.src.app.dto.transaction import HistoryDTO
from main_service.src.app.repositories.transaction import TransactionRepository


@pytest.mark.asyncio
class TestUserRepository:
    @pytest_asyncio.fixture
    async def repository(self, db_session):
        yield TransactionRepository(db_session)

    @pytest_asyncio.fixture
    async def create_user(self, db_session):
        await db_session.execute(
            insert(User).values(
                card_number='1111',
                balance=10,
                card_limit=1000,
                name='Ivan',
                age=20,
            )
        )
    
    @pytest_asyncio.fixture
    async def create_user_storage(self, db_session):
        await db_session.execute(
            insert(UserStorage).values(
                user_storage_id= 1,
                user_card_number='1111',
                is_active=True,
            )
        )
    
    @pytest_asyncio.fixture
    async def create_log_storage(self, db_session):
        await db_session.execute(
            insert(LogStorage).values(
                log_storage_id = 1,
                balance_log_id='1111',
                common_log_id ='1111',
            )
        )

    @pytest_asyncio.fixture
    async def create_transaction(self, db_session):
        await db_session.execute(
            insert(Transaction).values(
                log_storage_id = 1,
                user_storage_id= '1111',
            )
        )
    async def test_get_balance(self, repository, db_session, create_user, create_user_storage, create_log_storage, create_transaction):
        record = await repository.get_balance('1111')
        assert record.balance==10
    
    @pytest_asyncio.fixture
    async def create_balance_log(self, db_session):
        await db_session.execute(
            insert(BalanceLog).values(
                card_number = '1111',
                before = 10,
                after = 110,
                changes = 100,
                datetime_utc = datetime(2023,8,8,20,20,20),
            )
        )
    
    async def test_get_balance_history(
            self,
            repository,
            db_session,
            create_balance_log
    ):
        record = await repository.get_balance_history('1111',datetime(2020,8,8,20,20,20), datetime(2024,8,8,20,20,20))
        assert isinstance(record, HistoryDTO)
    
    async def test_withdrawal(
            self,
            repository,
            db_session,
    ):
        record = await repository.withdrawal('1111',10)
        assert record==200

    async def test_deposit(
            self,
            repository,
            db_session,
    ):
        record = await repository.withdrawal('1111',10)
        assert record==200
    
    async def test_change_limit(
            self,
            repository,
            db_session,
    ):
        record = await repository.change_limit('1111',2000)
        assert record.card_limit==2000