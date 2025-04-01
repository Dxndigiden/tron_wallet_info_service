# Микросервис TronInfo

## Описание

Микросервис TronInfo предоставляет информацию о кошельках в сети Tron. Он позволяет пользователям получать данные о балансе, bandwidth и energy по заданному адресу кошелька. Каждый запрос сохраняется в базе данных, что позволяет отслеживать историю запросов.

### Микросервис имеет два основных эндпоинта:

- *POST /wallet/info*: принимает адрес кошелька и возвращает информацию о нем, сохраняя данные в базе.
- *GET /wallets*: возвращает список последних запросов из базы данных с возможностью пагинации.

Для удобства использования доступна интерактивная документация API через Swagger, где можно протестировать эндпоинты.

## Используемые технологии

- Python 3.10.10
- FastAPI 0.115.12
- SQLAlchemy 2.0.40
- Async SQLite
- Alembic 1.15.2
- Uvicorn 0.34.0
- Tronpy 0.5.0
- Pytest 8.3.5

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

### Эндпоинт: POST /wallet/info

Этот эндпоинт позволяет получить информацию о кошельке в сети Tron.

#### Запрос

Для использования этого эндпоинта вам необходимо ввести адрес кошелька в формате, который начинается с "T" и содержит 34 символа.

![Пример запроса](https://raw.githubusercontent.com/Dxndigiden/tron_wallet_info_service/refs/heads/dev/img/request_example.PNG?token=GHSAT0AAAAAADA7WVPX3DHUONATRCQA5RNWZ7MDX7A)

#### Ответ

После успешного выполнения запроса вы получите ответ с информацией о кошельке, включая баланс, bandwidth и energy.

![Пример ответа](https://raw.githubusercontent.com/Dxndigiden/tron_wallet_info_service/refs/heads/dev/img/response_example.PNG?token=GHSAT0AAAAAADA7WVPXUYPLL7JPHNL6LOHEZ7MDYSQ)

Вы также можете проверить информацию о кошельке на [Tronscan](https://tronscan.org/#/address/адрес_кошелька), заменив `адрес_кошелька` на фактический адрес.

![Пример ответа](https://raw.githubusercontent.com/Dxndigiden/tron_wallet_info_service/refs/heads/main/img/tronscan.PNG?token=GHSAT0AAAAAADA7WVPWDBVYVCRPDRXNG4XEZ7MDZHQ)

---

### Эндпоинт: GET /wallets

Этот эндпоинт возвращает список последних запросов из базы данных с возможностью пагинации.

#### Запрос

Для использования этого эндпоинта вы можете указать параметры `skip` и `limit`, чтобы управлять пагинацией. Например:

- `skip`: количество записей, которые нужно пропустить (по умолчанию 0).
- `limit`: количество записей для возврата (по умолчанию 10).

![Пример запроса](https://raw.githubusercontent.com/Dxndigiden/tron_wallet_info_service/refs/heads/dev/img/pagination_example.PNG?token=GHSAT0AAAAAADA7WVPXEBPCP4UO3EIYZVD2Z7MDWUQ)

#### Ответ

Ответ будет содержать список кошельков, начиная с самых последних записей.

![Пример ответа](https://raw.githubusercontent.com/Dxndigiden/tron_wallet_info_service/refs/heads/dev/img/wallets_response_example.PNG?token=GHSAT0AAAAAADA7WVPW2PBMDJBTKSRQZMOIZ7MDZSQ)


## Как запускать тесты

Для запуска тестов используйте команду из корневой дирректории:

```
pytest
```

## Автор

[Денис Смирнов](https://github.com/dxndigiden)

