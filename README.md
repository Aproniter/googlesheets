# googlesheets
googlesheets to db

<h1 align="center">GoogleSheetsHelper</h1>


### Технологии
Python 3.9
Flask
Celery
Redis
Postgresql
Sqlalchemy
React
Docker
Docker-compose


### Запуск проекта
- В папку googlesheets\backend\.config добавить файл с конфигурацией сервисного аккаунта GoogleAPI с именем service_account.json

- В папку googlesheets\infra добавить .env файл с содержимым:
    - PG_URI=postgresql://<логин>:<пароль>@<хост>:<порт>/ordersDB
    - CELERY_BROKER_URL=redis://<хост>:<порт>/0
    - CELERY_RESULT_BACKEND=redis://<хост>:<порт>/0
    - REDIS_HOST=<хост>
    - REDIS_HOST=<порт>
    - TELEGRAM_TOKEN=токен телеграм-бота
    - CHAT_ID=id чата бота с нужным аккаунтом

- В папке googlesheets\infra запустите docker-compose:
    - sudo docker-compose up -d --build

### Description
GoogleSheetsHelper: получение данных из по расписанию GoogleSheets. Работа с данными на стороне сервера. Предоставление API для работы с БД. Простой дашборд на React. Уведомление через телеграм-бота по условию

**GoogleSheetsHelper API**
- <host>/orders - (GET) Получить все заказы из БД
- <host>/orders/<order_number> - (GET) Полусить из БД заказ по номеру
- <host>/orders?limit=<int> - (GET) Получить <limit> количество звказов
- <host>/orders?missed=1 - (GET) Получить просроченные заказы
- <host>/orders - (POST) Ручное добавление заказа (В теле запроса: {"order_number", "price_dollars", "price_rub", "delivery_time"})
 

