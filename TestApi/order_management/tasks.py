from celery import Celery
from sseclient import SSEClient
import logging 
import json
from order_management.models import Order


app = Celery('tasks', broker='redis://redis:6379/0')


@app.task
def update_values(data):
    try:
        data = json.loads(data)

        if Order.objects.filter(id=data.get('order').get('id')).exists():
            order = Order.objects.get(id=data.get('order').get('id'))
            order.status = data.get('order').get('status')
            order.save()
        print("Order saved")
        
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)


@app.task
def listen_sse_events():
    sse_url = "https://broker-api.sandbox.alpaca.markets/v2beta1/events/trades?since=2024-01-29T18%3A38%3A01.942282Z"
    headers = {
    "accept": "text/event-stream",
    "authorization": "Basic Q0s3NlFMWEZRUlFONEMxSzAxMTc6Qm1LdTZpT0t6V0lnQmhaaDhBYTRnVHlGdXhxYTFtMjZZZGtTTFA1eA=="
    }

    messages = SSEClient(sse_url, headers=headers)

    for msg in messages:
        if msg.event == 'message':
            update_values.delay(msg.data)


