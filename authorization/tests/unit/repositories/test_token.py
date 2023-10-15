import pytest
import pytest_asyncio
from sqlalchemy import insert

from authorization.src.app.db.models.user import User
from authorization.src.app.repositories.token import TokenRepository


@pytest.mark.asyncio
class TestTokenRepository:
    @pytest_asyncio.fixture
    async def repository(self, db_session):
        yield TokenRepository(db_session)

    @pytest_asyncio.fixture
    async def create_user(self, db_session):
        await db_session.execute(
            insert(User).values(
                user_id=2,
                login='any_login',
                password='any_password',
            )
        )

    async def test_create_token(self, repository, db_session, create_user):
        record = await repository.create_token(2)
        assert record.user_id==2
