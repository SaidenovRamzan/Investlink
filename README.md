Основной сервис Order Manager for Alpaca"

Описание
nvestlink Test API - это приложение, которое является оберткой для Alpaca API, предоставляющее различные функции для управления заказами на финансовых рынках.

Модуль order_management


## Функции

### 1. Просмотр заказов

За просмотр заказа отвечат класс ListOrders. Приложение предоставляет возможность просмотр текущих и исторических заказов пользователя на финансовых рынках. Пользователи могут получать информацию о статусе заказа, его исполнении, времени размещения и других релевантных параметрах. Мы принимаем accout_id и квери параметры, после чего валидируем их и отправляем к Alpaca, ответ от Alpaca возвращаем

### 2. Отмена заказа

За отмену заказа отвечат класс CancelOrder. Пользователи могут отменять существующие заказы на рынке, которые были отправлены через Alpaca API. Это позволяет пользователям реагировать на изменяющиеся условия рынка и адаптировать свои торговые стратегии в реальном времени. Заказ проходит валидацию и отправляется к Alpaca, при ответе 204 мы находим заказ у себя и удаляем

### 3. Создание заказа

За создание заказа отвечат класс CreateOrder. Приложение позволяет пользователям создавать новые заказы на финансовых рынках через Alpaca API. Пользователи могут указывать различные параметры заказа, такие как символ актива, объем, тип ордера (рыночный, лимитный и т. д.) и другие характеристики, необходимые для выполнения торговой операции. Заказ в начале проходит нашу валидацию, затем отправляется к Alpaca, она возвращает заказ и мы его сохраняем

# Установка

Для установки приложения следуйте простым инструкциям ниже:

1. Перейдите в каталог, где расположен файл `Dockerfile`:

```bash
cd путь_к_каталогу_где_Dockerfile 
```

Создайте файл .env на уровне manage.py

```bash
touch .env
```

Заполните данными  .env

```bash
API_KEY=CK76QLXFQRQN4C1K0117
API_SECRET=BmKu6iOKzWIgBhZh8Aa4gTyFuxqa1m26YdkSLP5x
Broker_id=5e62581b-1a60-4f8d-a950-4efa12d15be7

#DB config
DB_NAME='alpacaDB'
DB_USER='postgres'
DB_PASSWORD='postgres'
DB_HOST='postgres'
DB_PORT='5432'

#Redis
REDIS_PORT='6379'
REDIS_HOST='redis'
```

Запустите сборку образов Docker и запустите контейнеры в фоновом режиме с помощью следующих команд:

```bash
docker-compose build
docker-compose up -d
```

# Просмотр API

Вы можете ознакомиться со всеми доступными эндпоинтами и документацией API, перейдя по адресу:

http://localhost:8000/swagger/

Swagger предоставляет интерактивную документацию, которая поможет вам понять структуру и функциональность вашего API.

# Примечание:
При запуске программы, она начиет слушать SSE сообщений от Alpaca.
Для создания суперюзера, выполните следующую команду:

```bash

docker exec -it web /bin/bash 
python manage.py createsuperuser
```

Для установки тестовых данных заказов в базу данных, выполните следующую команду:

```bash

docker exec -it web /bin/bash 
python manage.py get_all_orders
```

Эта команда загрузит тестовые данные заказов в вашу базу данных.


Чтобы изменить статус всех заказов на "new" и проверить обновление через SSE соединение, выполните:

```bash

docker exec -it web /bin/bash 
python manage.py сhange_all_statuses
```

Эта команда изменит статус всех заказов на "new", что позволит вам наблюдать обновление через SSE соединение.


Чтобы накатить фикстуры ныжно пропичать

```bash

docker exec -it web /bin/bash 
python manage.py loaddata fixtures/initial_data.json
```
