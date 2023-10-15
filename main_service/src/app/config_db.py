"""Модуль для конфигурации переменных для БД."""
from dataclasses import dataclass


@dataclass
class PostgresConfig:
    """_summary_.

    Returns:
        _type_: _description_
    """

    login: str
    password: str
    host: str
    port: str
    db_name: str

    @property
    def url(self):
        """_summary_.

        Returns:
            _type_: _description_
        """
        return '{0}:{1}@{2}:{3}'.format(
            self.login,
            self.password,
            self.host,
            self.port,
        )

    @property
    def uri(self):
        """_summary_.

        Returns:
            _type_: _description_
        """
        return 'postgresql+asyncpg://{0}/{1}'.format(self.url, self.db_name)


@dataclass
class AppConfig:
    """."""

    postgres: PostgresConfig


app_config = AppConfig(
    postgres=PostgresConfig(  # noqa: S106
        login='postgres',
        password='1234',
        host='127.0.0.1',
        port='5432',
        db_name='main',
    ),
)
