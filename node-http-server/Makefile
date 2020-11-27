
IMAGE_NAME=m7dock/node-http-server
CONTAINER_NAME=file-server-castle
ROOT_FOLDER 	?= 	${HOME}/www


build-container:
	docker build -t ${IMAGE_NAME} .

stop:
	docker stop ${CONTAINER_NAME} || true

run: stop
	docker run --rm -d --name ${CONTAINER_NAME} -v ${ROOT_FOLDER}:/opt/www  -v ${HOME}/music:/opt/www/music  -p 18080:8080 ${IMAGE_NAME} /opt/www