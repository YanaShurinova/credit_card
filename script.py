from fastapi.openapi.utils import get_openapi

from authorization.src.app.main import app


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Swagger documentation",
        version="0.0.1",
        summary="",
        description="Данная схема описывает следующие эндпоинты:\n \
            auth - эндпоинт авторизации;\n\
            get_balance - эндпоинт, возвращающий балнс пользователя по номеру карты;\n\
            get_balance_history - эндпоинт, возвращающий историю баланса пользователя по номеру карты за определенный период времени;\n\
            withdrawal - эндпоинт, позволяющий списывать определенную сумму с баланса пользователя;\n\
            deposit - эндпоинт, позволяющий зачислять определенную сумму на счет пользователя;\n\
            verify - эндпоинт, проверяющий идентичность лиц человека по двум фотографиям.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

js = str(app.openapi())

with open('openapi.json', 'w') as outfile:
    outfile.write(js)