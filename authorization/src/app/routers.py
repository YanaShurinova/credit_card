"""Модуль для запуска сервиса."""
import sys
from typing import List

import aiofiles
import aiohttp
from aiokafka import AIOKafkaProducer
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    responses,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from prometheus_client import Counter, Histogram
from starlette.status import HTTP_200_OK

from authorization.src.app.adaptor import DatabaseConnection
from authorization.src.app.config import main_url
from authorization.src.app.dto import token
from authorization.src.app.dto.balance import BalanceDTO
from authorization.src.app.dto.history import HistoryDTO
from authorization.src.app.repositories.token import TokenRepository
from authorization.src.app.repositories.user import UserRepository

sys.path.append('C:\\Users\\Яна\\PycharmProjects\\credit_card')  # noqa: WPS342

api_router = APIRouter(prefix='/api')

session = DatabaseConnection().get_session()

requests_num = Counter(
    'auth_service_request_number',
    'Count number of requests',
    ['endpoint', 'http_status_code'],
)
ready_metric = Histogram(
    'auth_service_ready_metric',
    'Count number of requests',
    ['endpoint'],
)
change_limit_metric_success = Counter(
    'auth_service_change_limit_metric_success',
    'Count number of requests',
    ['result'],
)
change_limit_metric_fault = Counter(
    'auth_service_change_limit_metric_fault',
    'Count number of requests',
    ['result'],
)


@api_router.post('/auth', response_model=token.TokenDTO)
async def auth(
    form_data: OAuth2PasswordRequestForm = Depends(),  # noqa: B008
):
    """Хэндлер авторизации.

    Parameters:
        form_data: OAuth2PasswordRequestForm dependency

    Raises:
        HTTPException: исключения при обработке HTTP запросов

    Returns:
        str: токен
    """
    user = await UserRepository(session).get_user(
        form_data.username,
        form_data.password,
    )

    if not user:
        requests_num.labels('/api/auth', status.HTTP_400_BAD_REQUEST).inc()
        raise HTTPException(
            status_code=400,  # noqa: WPS432
            detail='Incorrect email or password',
        )
    requests_num.labels('/api/auth', status.HTTP_200_OK).inc()
    return await TokenRepository(session).create_token(user.user_id)


@api_router.get('/balance/{card_number}', response_model=BalanceDTO)
async def get_balance(card_number: str):
    """Хэндлер получения баланса по номеру карты.

    Parameters:
        card_number (str): номер карты

    Returns:
        json: {'balance': balance}
    """
    requests_num.labels('/api/balance/', status.HTTP_200_OK).inc()
    session_cl = aiohttp.ClientSession(raise_for_status=True)
    async with session_cl.get(
        '{0}/api/balance/{1}'.format(main_url, card_number),
    ) as resp:
        response = await resp.json()
    balance = response.get('balance')
    return {'balance': balance}


@api_router.get(
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
    requests_num.labels('/api/balance/history/', status.HTTP_200_OK).inc()
    session_cl = aiohttp.ClientSession(raise_for_status=True)
    async with session_cl.get(
        '{0}/api/balance/history/{1}'.format(main_url, card_number),
        params={'data_from': data_from, 'data_to': data_to},
    ) as resp:
        response = await resp.json()
    return response


@api_router.post('/withdrawal')
async def withdrawal(card_number: str, amount: int):
    """Хэндлер списания.

    Parameters:
        card_number (str): номер карты
        amount (int): сумма списания

    Returns:
        str: статус
    """
    requests_num.labels('/api/withdrawal', status.HTTP_200_OK).inc()
    session_cl = aiohttp.ClientSession(raise_for_status=True)
    resp = await session_cl.post(
        '{0}/api/withdrawal/'.format(main_url),
        params={'card_number': card_number, 'amount': amount},
    )
    return resp.status


@api_router.post('/deposit')
async def deposit(card_number: str, amount: int):
    """Хэндлер зачисления.

    Parameters:
        card_number (str): номер карты
        amount (int): сумма зачисления

    Returns:
        str: статус
    """
    requests_num.labels('/api/deposit', status.HTTP_200_OK).inc()
    session_cl = aiohttp.ClientSession(raise_for_status=True)
    resp = await session_cl.post(
        '{0}/api/deposit/'.format(main_url),
        params={'card_number': card_number, 'amount': amount},
    )
    return resp.status


@api_router.post('verify')
async def verify(  # noqa: WPS217
    user_id: int,
    card_number: str,
    files: List[UploadFile] = File(...),  # noqa: B008
):
    """Хэндлер верификации.

    Parameters:
        user_id (int): id банковского пользователя
        card_number (str): номер карты
        files (List[UploadFile], optional): изображения селфи и документа. Defaults to File(...).  # noqa: E501

    Raises:
        HTTPException: исключение при обработке запроса (не авторизован)

    Returns:
        str: статус
    """
    token_res = await TokenRepository(session).get_by_id(user_id)
    if token_res is None:
        change_limit_metric_fault.labels('fault').inc()
        raise HTTPException(
            status_code=401,  # noqa: WPS432
            detail='Пользователь не авторизован',
        )
    path1 = 'C:\\Users\\Яна\\PycharmProjects\\credit_card\\images\\{0}'.format(files[0].filename)  # noqa: WPS342, E501
    path2 = 'C:\\Users\\Яна\\PycharmProjects\\credit_card\\images\\{0}'.format(files[1].filename)  # noqa: WPS342, E501
    await save_image(files[0], path1)
    await save_image(files[1], path2)
    producer = AIOKafkaProducer()
    await producer.start()
    event = ({
        'card_number': card_number,
        'file1_path': path1,
        'file2_path': path2,
    })
    await producer.send(
        topic='verify',
        value=bytes(
            str(event),
            encoding='utf-8',
        ))
    await producer.stop()
    change_limit_metric_success.labels('success').inc()
    return HTTP_200_OK


async def save_image(image, path: str):
    """Метод сохранения файла на диск.

    Parameters:
        image (_type_): файл
        path (str): путь записи
    """
    async with aiofiles.open(path, 'wb') as out_file:
        content = await image.read()  # noqa: WPS110
        await out_file.write(content)

is_live = True


@api_router.get('/ready')
async def ready():
    """Метод для пробы.

    Returns:
        _type_: response
    """
    ready_metric.labels(
        '/ready',
    ).observe(
        responses.Response(status_code=status.HTTP_200_OK),
    )
    return responses.Response(status_code=status.HTTP_200_OK)


@api_router.get('/live')
async def live():
    """Метод для пробы.

    Returns:
        _type_: response
    """
    global is_live  # noqa: WPS420
    if is_live:
        return responses.Response(status_code=status.HTTP_200_OK)
    return responses.Response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@api_router.get('kill_live')
async def kill_live():
    """Метод закрытия пробы.

    Returns:
        _type_: response
    """
    global is_live  # noqa: WPS420
    is_live = False  # noqa: WPS442
    return responses.Response(status_code=status.HTTP_200_OK)
