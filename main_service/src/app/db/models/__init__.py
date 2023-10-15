import sys

sys.path.append('C:\\Users\\Яна\\PycharmProjects\\credit_card')  # noqa: WPS342
from main_service.src.app.db.models.balance_log import BalanceLog
from main_service.src.app.db.models.base import Base
from main_service.src.app.db.models.common_log import CommonLog
from main_service.src.app.db.models.log_storage import LogStorage
from main_service.src.app.db.models.transaction import Transaction
from main_service.src.app.db.models.user import User
from main_service.src.app.db.models.user_storage import UserStorage
