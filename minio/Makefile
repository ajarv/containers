

WORKDIR=$(shell pwd)
CONTAINER_NAME=minio
MINIO_ACCESS_KEY=brightangel
MINIO_SECRET_KEY=northkaibab
DATA_DIR=/var/lib/data/minio-data
stop:
	docker rm -f ${CONTAINER_NAME} || true
run: stop
	docker pull minio/minio:edge
	docker run --rm -d --name ${CONTAINER_NAME} -p 9000:9000 \
	-e "MINIO_ACCESS_KEY=${MINIO_ACCESS_KEY}" \
	-e "MINIO_SECRET_KEY=${MINIO_SECRET_KEY}" \
	-v ${DATA_DIR}:/data minio/minio:edge server /data
