from flask import Flask,request,jsonify
from minio import Minio
import sys
import os
import shutil
import queue
import time
import threading
import logging
import photo
import my_tasks

task_queue = queue.Queue()
logger = logging.getLogger(__file__)


def do_tasks(buc,key):
    try:
        logger.info(f'Working on {buc} {key}')
        cataloged_file = my_tasks.move_to_catalog_folder(key)
        if cataloged_file:
            if photo.JPGPAT.match(cataloged_file) and my_tasks.task_make_tn(cataloged_file):
                logger.info(f"Created Thumbnail {key}")
            my_tasks.task_remove_s3_object(buc,key)
            logger.info(f"Removed key {key}")
        logger.info(f'Done {buc} {key}')
    except:
        logger.exception(f'Failed {buc} {key}')
        pass

def worker():
    while True:
        (buc,key,valid_after,) = task_queue.get()
        delay = valid_after -  time.time()
        if delay > 0 :
            logger.info(f'Will work on {buc} {key} in {delay} sec')
            time.sleep(delay)
        do_tasks(buc,key)
        task_queue.task_done()

# turn-on the worker thread
threading.Thread(target=worker, daemon=True).start()

import json 
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hey, we have Flask in a Docker container!'

@app.route('/minio-event', methods=['POST', 'GET'])
def main():
    if request.method == 'HEAD':
        return ''
    payload = request.get_json()
    obj = payload['Records'][0]['s3']['object']['key']
    buc = payload['Records'][0]['s3']['bucket']['name']
    key = f"{buc}/{obj}"
    q.put((buc,key,time.time()+10,))
    logger.info(f"Queued up key {key}")
    return jsonify({'ok':True})


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    my_tasks.task_enqueue_bucket('images',task_queue)

    app.run(debug=False, host='0.0.0.0')
    