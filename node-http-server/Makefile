
IMAGE_NAME=m7dock/node-http-server
CONTAINER_NAME=file-server-castle

build-container:
	docker build -t ${IMAGE_NAME} .

stop:
	docker stop ${CONTAINER_NAME} || true

run: stop
	docker run --rm -d --name ${CONTAINER_NAME} -v ${HOME}/www:/opt/www  -v ${HOME}/music:/opt/www/music  -p 18080:8080 ${IMAGE_NAME} /opt/www