



run:
	docker pull minio/minio:edge
	docker run -p 9000:9000 -v $(pwd)/data:/data minio/minio:edge server /data