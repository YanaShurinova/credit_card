"""Модуль для запуска сервиса."""
import sys
from contextlib import asynccontextmanager

import uvicorn
from aiohttp import ClientSession
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from prometheus_client import make_asgi_app
from starlette.middleware.base import BaseHTTPMiddleware

from authorization.src.app.middlewares import metrics_middleware
from authorization.src.app.routers import api_router

sys.path.append('C:\\Users\\Яна\\PycharmProjects\\credit_card')  # noqa: WPS342


@asynccontextmanager
async def lifespan(app: FastAPI):
    """lifespan.

    Parameters:
        app (FastAPI): app

    Yields:
        ClientSession: сессия
    """
    session = ClientSession()
    kafka_producer = AIOKafkaProducer()
    await kafka_producer.start()
    yield {'client_sesiion': session, 'kafka_producer': kafka_producer}
    await session.close()
    await kafka_producer.stop()

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
metrics_app = make_asgi_app()
app.mount('/metrics', metrics_app)
# метрика для подсчета продолжительности запроса
app.add_middleware(BaseHTTPMiddleware, dispatch=metrics_middleware)
if __name__ == 'main':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=24023,  # noqa: WPS432
        reload=True,
    )
