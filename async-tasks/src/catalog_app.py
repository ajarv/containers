import os
from celery import Celery
import time

import celery_cfg
import thumbs_service

from file_service import FileService
from tags_service import TagServiceClient


    

# app = Celery('ztasks', broker=os.environ.get('AMQP_URL','pyamqp://guest:guest@libra:5672'))
app = Celery('pintask',broker_url = celery_cfg.broker_url)


fileService = FileService()
tagServiceClient = TagServiceClient()
@app.task
def add_file_tags(file_path,tags=[]):
    print(f"calling: add_file_tags({file_path=},{tags=})")
    if file_path != None:
        return tagServiceClient.add_tags(file_path,tag_list=tags)
    return None

@app.task
def minio_fetch_file(bucket_name,object_key):
    return fileService.download_file(bucket_name,object_key)

@app.task
def make_thumbnails(file_path):
    thumbs_service.make_thumbnails(file_path)


@app.task
def add(x, y):
    time.sleep(3)
    result = x + y + 33
    print(f"{result=}")
    return dict(result=result)

