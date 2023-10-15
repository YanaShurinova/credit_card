"""Модуль для подключения к БД."""
from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from authorization.src.app.config_db import app_config


class DatabaseConnection:
    """Класс для подключения к БД."""

    def __init__(self, config=app_config):
        """_summary_.

        Args:
            config (_type_, optional): _description_. Defaults to app_config.
        """
        _engine = create_async_engine(  # noqa: WPS122
            url=config.postgres.uri,
        )
        async_session_factory = sessionmaker(
            _engine,  # noqa: WPS121
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self._session_generator = async_scoped_session(
            async_session_factory,
            scopefunc=current_task,
        )

    def get_session(self) -> AsyncSession:
        """_summary_.

        Returns:
            AsyncSession: _description_
        """
        return self._session_generator()
