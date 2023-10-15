"""Модуль для подключения сервиса к БД."""
from src.dto.models.log import LogStorage
from src.dto.models.transactions import Transactions
from src.dto.models.user_storage import UserStorage

log_storage = LogStorage()
user_storage = UserStorage()
transactions = Transactions(user_storage, log_storage)
tokens = {}
