


```bash

docker run \
  -p 9000:9000 \
  -p 9001:9001 \
  -v /mnt/ssd/data:/data \
  -e "MINIO_ROOT_USER=kalpa" \
  -e "MINIO_ROOT_PASSWORD=rekongpeo" \
  quay.io/minio/minio server /data --console-address "192.168.0.11:9001"


## Test
docker build -t ptasks ./listener
docker run -it --rm -v /mnt/ssd/avashist/PhotoVault/vault:/data-out ptasks python my_tasks.py

```


mc admin config set minio notify_webhook:1 queue_limit="0"  endpoint="http://minio-listener:5000/minio-event" queue_dir=""

mc mb minio/images

mc event add minio/images arn:minio:sqs::1:webhook --event put --suffix .jpg
mc event add minio/images arn:minio:sqs::1:webhook --event put --suffix .jpg


mc event add minio/images arn:minio:sqs::1:webhook --event put --suffix .JPG


mc event add minio/images arn:aws:sqs:us-west-2:444455556666:your-queue --event replica,ilm


MINIO_HOST=192.168.0.11 MINIO_PORT=9000 MINIO_ACCESS_KEY=kalpa MINIO_SECRET_KEY=rekongpeo node presign-server.js


```bash
mc admin config set minio notify_webhook:1 queue_limit="0"  endpoint="http://minio-listener:5000/minio-event" queue_dir=""



set MINIO_NOTIFY_AMQP_ENABLE_one="on"
set MINIO_NOTIFY_AMQP_URL_one="amqp://guest:guest@rabbitmq:5672"
set MINIO_NOTIFY_AMQP_EXCHANGE_one="rabbit"

set MINIO_NOTIFY_AMQP_ENABLE_<IDENTIFIER>="on"
set MINIO_NOTIFY_AMQP_URL_<IDENTIFIER>="<ENDPOINT>"
set MINIO_NOTIFY_AMQP_EXCHANGE_<IDENTIFIER>="<string>"
set MINIO_NOTIFY_AMQP_EXCHANGE_TYPE_<IDENTIFIER>="<string>"
set MINIO_NOTIFY_AMQP_ROUTING_KEY_<IDENTIFIER>="<string>"
set MINIO_NOTIFY_AMQP_MANDATORY_<IDENTIFIER>="<string>"
set MINIO_NOTIFY_AMQP_DURABLE_<IDENTIFIER>="<string>"
set MINIO_NOTIFY_AMQP_NO_WAIT_<IDENTIFIER>="<string>"
set MINIO_NOTIFY_AMQP_INTERNAL_<IDENTIFIER>="<string>"
set MINIO_NOTIFY_AMQP_AUTO_DELETED_<IDENTIFIER>="<string>"
set MINIO_NOTIFY_AMQP_DELIVERY_MODE_<IDENTIFIER>="<string>"
set MINIO_NOTIFY_AMQP_QUEUE_DIR_<IDENTIFIER>="<string>"
set MINIO_NOTIFY_AMQP_QUEUE_LIMIT_<IDENTIFIER>="<string>"
set MINIO_NOTIFY_AMQP_COMMENT_<IDENTIFIER>="<string>"



mc admin config get libra notify_webhook 
```

amqp://lukhnow:banglore@rabbitmq:5672




mc event add libra/images arn:minio:sqs::one:amqp --event put --suffix .JPG

mc event add --event "put,delete" libra/images arn:aws:sqs::one:amqp  --suffix .JPG

mc event list libra libra/images arn:aws:sqs::one:amqp


mc admin config set libra notify_webhook:two queue_limit="0"  endpoint="http://minio-listener:5000/minio-event" queue_dir="/home/events"

mc event add libra/images arn:minio:sqs::two:webhook --event put --suffix .JPG
