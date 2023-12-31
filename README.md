# README
Данный проект является REST API приложением по бэкенду кредитной карты.
Приложение состоит из 3х микросервисов:
  - сервис авторизации, банковский сотрудник может пройти авторизацию и запрашивать необходимую информацию по клиенту банка через основной сервис;
  - основной сервис, который обрабатывает все запросы:
      + get_balance - получение баланса по номеру карты;
      + get_balance_history - получение истории баланса по номеру карты в определенный промежуток времени;
      + withdrawal - списание конкретной суммы с баланса пользователя по номеру карты;
      + deposit - зачисление конкретной суммы на баланса пользователя по номеру карты:
      + change_limit - метод, который изменяет лимит пользователя.
  - сервис верификации, содержит один метод - верификация пользователя по изображению, использует библиотеку DeepFace, в случае прохождения запрашивает изменение лимита через основной сервис.
Сервисы авторизации и верификации связаны друг с другом через брокер сообщений - Kafka

## Используемые технологии:
  1. Python 3.10
  2. FastAPI, PostgreSQL
  3. Для миграций - SQLAlchemy и Alembic
  4. Docker, Kubernetes
  5. Pytest, pytest_asyncio
