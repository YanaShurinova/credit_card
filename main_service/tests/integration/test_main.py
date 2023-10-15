import pytest
import pytest_asyncio
from aiohttp import ClientSession, TCPConnector
from sqlalchemy import insert

from main_service.src.app.db.models.log_storage import LogStorage
from main_service.src.app.db.models.transaction import Transaction
from main_service.src.app.db.models.user import User
from main_service.src.app.db.models.user_storage import UserStorage
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
                card_number='3333',
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
                user_storage_id= 3,
                user_card_number='3333',
                is_active=True,
            )
        )
    
    @pytest_asyncio.fixture
    async def create_log_storage(self, db_session):
        await db_session.execute(
            insert(LogStorage).values(
                log_storage_id = 3,
                balance_log_id='3333',
                common_log_id ='3333',
            )
        )

    @pytest_asyncio.fixture
    async def create_transaction(self, db_session):
        await db_session.execute(
            insert(Transaction).values(
                log_storage_id = 3,
                user_storage_id= '3333',
            )
        )
    async def test_get_balance(self, repository, db_session, create_user, create_user_storage, create_log_storage, create_transaction):
        record = await repository.get_balance('3333')
        assert record.balance==10

    async def get_metrics():
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            resp = await session.get('https://127.0.0.1:24023/metrics')
            print(await resp.text())
            assert resp.text is not None
