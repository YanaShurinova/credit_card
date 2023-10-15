"""Метрика для подсчета времени."""
import time

from fastapi import Request, Response
from prometheus_client import Histogram
from starlette.status import HTTP_400_BAD_REQUEST

request_latency_histogram = Histogram(
    'auth_service_request_latency_histogram',  # Название метрики
    'Request latency.',  # Документация метрики
    ['operation', 'http_status_code', 'error'],  # Лейблы
)


async def metrics_middleware(request: Request, call_next):
    """Middleware для реализации логгирования времени выполнения запроса.

    Parameters:
        request: req
        call_next: req

    Returns:
        _type_: response
    """
    start_time = time.monotonic()
    response: Response = await call_next(request)
    operation = f'{request.method} {request.url.path}'  # noqa: WPS237, WPS305
    request_latency_histogram.labels(
        operation,
        response.status_code,
        response.status_code >= HTTP_400_BAD_REQUEST,
    ).observe(
        time.monotonic() - start_time,
    )
    return response
