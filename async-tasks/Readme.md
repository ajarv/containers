


```bash

docker build -t s3-listener .

docker run --rm -it \
  -v /mnt/ssd/data:/data \
  -v $(pwd):/usr/src/app \
  -e "AMQP_HOSTNAME=libra" \
  s3-listener /bin/sh -c 'ls'

docker run --rm -it \
  -v /mnt/ssd/data:/data \
  -v /mnt/5tb/Photovault/vault:/data-out \
  -v $(pwd):/usr/src/app \
  -e "AMQP_HOSTNAME=libra" \
  s3-listener /bin/sh -c 'python src/s3_event_listener.py'


celery -A catalog_task  -b  pyamqp://guest:guest@libra:5672 worker  --loglevel=INFO


. ~/.bash_profile ; py39
```