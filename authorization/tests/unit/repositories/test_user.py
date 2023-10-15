import pytest
import pytest_asyncio
from sqlalchemy import insert

from authorization.src.app.db.models.user import User
from authorization.src.app.repositories.user import UserRepository


@pytest.mark.asyncio
class TestUserRepository:
    @pytest_asyncio.fixture
    async def repository(self, db_session):
        yield UserRepository(db_session)

    @pytest_asyncio.fixture
    async def create_user(self, db_session):
        await db_session.execute(
            insert(User).values(
                login='any_login',
                password='any_password',
            )
        )
    async def test_get_user(self, repository, db_session, create_user):
        record = await repository.get_user('any_login', 'any_password')
        assert record.login=='any_login'
        assert record.password=='any_password'
