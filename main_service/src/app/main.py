"""Основной модуль."""
import uvicorn
from fastapi import FastAPI

from main_service.src.app.routers import main_router

app = FastAPI()
app.include_router(main_router)


if __name__ == 'main':
    uvicorn.run(
        'src.app.main:app',
        host='127.0.0.1',
        port=24123,  # noqa: WPS432
        reload=True,
    )
