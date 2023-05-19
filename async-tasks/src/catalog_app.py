import os
from celery import Celery
import time

# app = Celery('ztasks', broker=os.environ.get('AMQP_URL','pyamqp://guest:guest@libra:5672'))
app = Celery('pintask')

@app.task
def add(x, y):
    time.sleep(3)
    result = x + y + 33
    print(f"{result=}")
    return dict(result=result)