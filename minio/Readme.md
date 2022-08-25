


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


mc event add minio/images arn:minio:sqs::1:webhook --event put --suffix .*





MINIO_HOST=192.168.0.11 MINIO_PORT=9000 MINIO_ACCESS_KEY=kalpa MINIO_SECRET_KEY=rekongpeo node presign-server.js