import datetime
import os
import pika
import sys
import json
import time
import logging
from mutil import get_cfg_val
import file_service
import catalog_app
from celery import group
# import celery_cfg

LOGGER = logging.getLogger(__file__.split('/')[-1])


class ExchangeAgent:
    def __init__(self, **kwargs) -> None:
        credentials = pika.PlainCredentials(
            get_cfg_val(kwargs, os.environ, 'AMQP_USERNAME', 'guest'),
            get_cfg_val(kwargs, os.environ, 'AMQP_PASSWORD', 'guest'))
        parameters = pika.ConnectionParameters(
            get_cfg_val(kwargs, os.environ, 'AMQP_HOSTNAME', 'libra'),
            int(get_cfg_val(kwargs, os.environ, 'AMQP_PORT', '5672')), '/',
            credentials)
        self.queue_name = get_cfg_val(kwargs, os.environ, 'AMQP_QUEUE',
                                      's3-event')
        self.exchange = "amq.direct"
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        LOGGER.info(f"Init OK {parameters=} , {self.queue_name=}")
        self.event_callback = None
        self.setup()

    def setup(self):
        self.channel.queue_declare(queue=self.queue_name, durable=True, 
                                   exclusive=False, auto_delete=False)
        self.channel.queue_bind(self.queue_name,self.exchange,self.queue_name)
        LOGGER.info("Exchange Setup")
    def begin(self,event_callback):
        self.event_callback = event_callback
        self.channel.basic_consume(queue=self.queue_name,
                                   on_message_callback=self.callback,
                                   auto_ack=False)
        LOGGER.info(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    # channel.queue_declare(queue='wall.01')
    def callback(self, ch, method, properties, body):
        # print(f"callback: {body=}, {properties=}, {method=}, {ch=}")
        try:
            event_data = json.loads(body)
            # print(f"{event_data=}")
            # print(json.dumps(json.loads(body),indent='\t'))
            # self.record_processor_cb(event_data)
            
            bucket_name = event_data['Records'][0]['s3']['bucket']['name']
            object_name = event_data['Records'][0]['s3']['object']['key']
            event_name = event_data['Records'][0]['eventName']
            if self.event_callback:
                self.event_callback(event_name,bucket_name, object_name)
            ch.basic_ack(delivery_tag = method.delivery_tag) ### <--- this one
        except:
            LOGGER.exception(f"Error processing rabbit event")
            pass
        # print(json.dumps(json.loads(body),indent='\t'))
        # ch.basic_ack(delivery_tag = method.delivery_tag) ### <--- this one


def main():
    # _FileService = file_service.FileService()

    # catalog_app.app.conf.update(broker_url = celery_cfg.broker_url)

    tn_task = catalog_app.make_thumbnails.s()
    def event_callback(event_name,bucket_name, object_key):
        if "ObjectCreated" in  event_name :
            upload_date_tag = f"ns0:upload-date:{datetime.date.today().isoformat()}"
            tag_task = catalog_app.add_file_tags.s(tags=[upload_date_tag])
            job = group(tag_task,tn_task)
            # catalog_app.minio_fetch_file.apply_async((bucket_name,object_key,),link=tag_task)
            catalog_app.minio_fetch_file.apply_async((bucket_name,object_key,),link=job)
            LOGGER.info(
                f"Enqued {bucket_name=}, {object_key=}, {event_name=}")
        pass
    _ExchangeAgent = ExchangeAgent()
    _ExchangeAgent.begin(event_callback)
        
if __name__ == "__main__":   
    logging.basicConfig(    format = '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
                        level=logging.INFO)
    main()