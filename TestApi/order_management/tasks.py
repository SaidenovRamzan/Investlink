from celery import Celery
from sseclient import SSEClient
import logging 
import json
from order_management.models import Order

# Создание экземпляра Celery
app = Celery('tasks', broker='redis://redis:6379/0')

# Задача для обновления значений на основе полученных данных
@app.task
def update_values(data):
    # Ваш код для обновления значений на основе полученных данных
    print("Received data:", data)
    data = json.loads(data)
    
    # if Order.objects.filter(id=data.get('id')).exists():
    #     order = Order.objects.get(id=data.get('id'))
    #     order.status = data.get('status')
    #     order.save()
    
    # else:
    #     Order.objects.create(**data)
    logging.info(data)
    print(f"{data=}====================================")

# Задача для прослушивания SSE событий
@app.task
def listen_sse_events():
    # URL SSE endpoint, который вы хотите прослушивать
    sse_url = "https://broker-api.sandbox.alpaca.markets/v2beta1/events/trades?since=2024-01-16T18%3A38%3A01.942282Z"
    headers = {
    "accept": "text/event-stream",
    "authorization": "Basic Q0s3NlFMWEZRUlFONEMxSzAxMTc6Qm1LdTZpT0t6V0lnQmhaaDhBYTRnVHlGdXhxYTFtMjZZZGtTTFA1eA=="
    }
    # Подключение к SSE endpoint
    messages = SSEClient(sse_url, headers=headers)

    # Прослушивание событий
    for msg in messages:
        if msg.event == 'message':
            # Вызов задачи для обновления значений
            update_values.delay(msg.data)


