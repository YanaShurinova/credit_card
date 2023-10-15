"""Модуль для запуска сервиса."""
import sys
from datetime import datetime

from fastapi import APIRouter, responses, status
from starlette.status import HTTP_200_OK

from main_service.src.app.adaptor import DatabaseConnection
from main_service.src.app.dto.transaction import BalanceDTO, HistoryDTO
from main_service.src.app.repositories.transaction import TransactionRepository

sys.path.append('C:\\Users\\Яна\\PycharmProjects\\credit_card')  # noqa: WPS342

main_router = APIRouter(prefix='/api')

session = DatabaseConnection().get_session()


@main_router.get('/balance/{card_number}', response_model=BalanceDTO)
async def get_balance(card_number: str):
    """Хэндлер получения баланса по номеру карты.

    Parameters:
        card_number (str): номер карты

    Returns:
        json: {'balance': balance}
    """
    return await TransactionRepository(session).get_balance(card_number)


@main_router.get(
    '/balance/history/{card_number}',
    response_model=HistoryDTO,
)
async def get_history(card_number, data_from: str, data_to: str):
    """Хэндлер получения историия баланса.

    Parameters:
        card_number (str): номер карты
        data_from (str): дата начала
        data_to (str): дата конца

    Returns:
        LogStorage: история
    """
    data_from = datetime.strptime(data_from, '%m %d %Y %H:%M:%S')
    data_to = datetime.strptime(data_to, '%m %d %Y %H:%M:%S')
    return await TransactionRepository(session).get_balance_history(
        card_number,
        data_from,
        data_to,
    )


@main_router.post('/withdrawal')
async def withdrawal(card_number: str, amount: int):
    """Хэндлер списания.

    Parameters:
        card_number (str): номер карты
        amount (int): сумма списания

    Returns:
        str: статус
    """
    await TransactionRepository(session).withdrawal(card_number, amount)
    return HTTP_200_OK


@main_router.post('/deposit')
async def deposit(card_number: str, amount: int):
    """Хэндлер зачисления.

    Parameters:
        card_number (str): номер карты
        amount (int): сумма зачисления

    Returns:
        str: статус
    """
    await TransactionRepository(session).deposit(card_number, amount)
    return HTTP_200_OK


@main_router.post('/change_limit')
async def change_limit(card_number: str, new_limit: int):
    """Метод изменения лимита.

    Parameters:
        card_number (str): номер карты
        new_limit (int): новый лимит

    Returns:
        str: статус
    """
    await TransactionRepository(session).change_limit(card_number, new_limit)
    return HTTP_200_OK


is_live = True


@main_router.get('/ready')
async def ready():
    """Проба реди.

    Returns:
        _type_: response
    """
    return responses.Response(status_code=status.HTTP_200_OK)


@main_router.get('/live')
async def live():
    """Метод пробы.

    Returns:
        _type_: response
    """
    global is_live  # noqa: WPS420
    if is_live:
        return responses.Response(status_code=status.HTTP_200_OK)
    return responses.Response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@main_router.get('kill_live')
async def kill_live():
    """Закрытие пробы.

    Returns:
        _type_: response
    """
    global is_live  # noqa: WPS420
    is_live = False  # noqa: WPS442
    return responses.Response(status_code=status.HTTP_200_OK)
