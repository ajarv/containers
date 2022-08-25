from flask import Flask,request,jsonify
from minio import Minio
import time
import logging
import my_tasks

logger = logging.getLogger(__file__)


import json
app = Flask(__name__)

@app.route('/',methods=['POST', 'GET','HEAD'])
def hello_world():
    if request.method == 'HEAD':
        return ''
    if request.method == 'GET':
        'Hey, we have Flask in a Docker container!'

    payload = request.get_json()
    object_name = payload['Records'][0]['s3']['object']['key']
    bucket_name = payload['Records'][0]['s3']['bucket']['name']
    my_tasks.task_enqueue_key(bucket_name, object_name)
    return jsonify({'ok':True})

@app.route('/minio-event', methods=['POST', 'GET','HEAD'])
def main():
    if request.method == 'HEAD':
        return ''
    payload = request.get_json()
    object_name = payload['Records'][0]['s3']['object']['key']
    bucket_name = payload['Records'][0]['s3']['bucket']['name']
    my_tasks.task_enqueue_key(bucket_name, object_name)
    return jsonify({'ok':True})


if __name__ == '__main__':
    format = '%(asctime)s %(levelname)-8s %(name)-15s %(message)s'
    logging.basicConfig(format=format, level=logging.INFO)
    my_tasks.task_enqueue_bucket('images')
    app.run(debug=False, host='0.0.0.0')
