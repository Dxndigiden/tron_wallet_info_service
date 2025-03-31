# Микросервис TronInfo

## Описание

Микросервис TronInfo предоставляет информацию о кошельках в сети Tron. Он позволяет пользователям получать данные о балансе, bandwidth и energy по заданному адресу кошелька. Каждый запрос сохраняется в базе данных, что позволяет отслеживать историю запросов.

Микросервис имеет два основных эндпоинта:
- *POST /wallet/info*: принимает адрес кошелька и возвращает информацию о нем, сохраняя данные в базе.
- *GET /wallets*: возвращает список последних запросов из базы данных с возможностью пагинации.

Для удобства использования доступна интерактивная документация API через Swagger, где можно протестировать эндпоинты.

## Используемые технологии

- Python 3.9+
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- Uvicorn
- Tronpy
- Pytest (для тестирования)

## Как запустить проект

1. Клонировать репозиторий и создать виртуальное окружение:

```
git clone git@github.com:dxndigiden/tron_wallet_info_service.git
cd tron_wallet_info_service
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate  # для Windows
```

2. Установить зависимости:

```
pip install --upgrade pip
pip install -r requirements.txt
```

3. Создать и заполнить файл `.env`:
   Используйте файл `.env.example` в качестве примера.

4. Выполнить миграции:

```
alembic upgrade head
```

5. Запустить приложение:

```
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Использование Swagger

Чтобы протестировать API, зайдите на страницу Swagger по адресу [http://127.0.0.1:8000/swagger](http://127.0.0.1:8000/swagger). 

- *POST /wallet/info*: здесь вы можете отправить запрос с адресом кошелька и получить информацию о нем.
- *GET /wallets*: используйте этот эндпоинт, чтобы получить список последних запросов из базы данных. Вы можете указать параметры для пагинации.


## Как запускать тесты

Для запуска тестов используйте команду:

```
pytest
```

## Автор

[Денис Смирнов](https://github.com/dxndigiden)
