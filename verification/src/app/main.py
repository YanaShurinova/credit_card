"""Модуль для запуска сервиса."""
import asyncio
import json
from contextlib import asynccontextmanager

import aiojobs
import uvicorn
from aiokafka import AIOKafkaConsumer
from deepface import DeepFace
from fastapi import FastAPI, responses, status

from verification.src.app import utils

resources = {}


async def verify_kafka():
    """Обработка в брокере.

    Returns:
        bool: статус верификации
    """
    consumer: AIOKafkaConsumer = resources.get('kafka_consumer')
    await asyncio.sleep(1)
    resp = await consumer.getone()
    resp = json.loads(resp.value.decode('utf-8').replace("'", '"'))
    file1 = utils.read_image(resp.get('file1_path'))
    file2 = utils.read_image(resp.get('file2_path'))
    return utils.verify(resp.get('card_number'), file1, file2)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """lifespan.

    Parameters:
        app (FastAPI): fastapi

    Yields:
        yield
    """
    scheduler = aiojobs.Scheduler()
    kafka_consumer = AIOKafkaConsumer('verify')
    await kafka_consumer.start()
    resources['kafka_consumer'] = kafka_consumer
    await scheduler.spawn(verify_kafka())
    yield
    await kafka_consumer.stop()
    await scheduler.close()
    resources.clear()


app = FastAPI(lifespan=lifespan)
model = DeepFace.build_model('Facenet')

is_live = True


@app.get('/ready')
async def ready():
    """Проба реди.

    Returns:
        _type_: response
    """
    return responses.Response(status_code=status.HTTP_200_OK)


@app.get('/live')
async def live():
    """Проба жизни.

    Returns:
        _type_: response
    """
    global is_live  # noqa: WPS420
    if is_live:
        return responses.Response(status_code=status.HTTP_200_OK)

    return responses.Response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@app.get('kill_live')
async def kill_live():
    """Закрытие пробы.

    Returns:
        _type_: response
    """
    global is_live  # noqa: WPS420
    is_live = False  # noqa: WPS442
    return responses.Response(status_code=status.HTTP_200_OK)


if __name__ == 'main':
    uvicorn.run(
        'src.app.main:app',
        host='127.0.0.1',
        port=24223,  # noqa: WPS432
        reload=True,
    )
