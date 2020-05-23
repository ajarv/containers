

WORKDIR=$(shell pwd)

run:
	docker pull minio/minio:edge
	docker run --rm -d --name minio -p 9000:9000 -e MINIO_ACCESS_KEY:phantom -e MINIO_SECRET_KEY:ranch -v ${WORKDIR}/data:/data minio/minio:edge server /data