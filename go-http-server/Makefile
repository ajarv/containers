
IMAGE_NAME='m7dock/go-http-server'
CONTAINER_NAME='file-server-ghana'

build-container:
	docker build -t ${IMAGE_NAME} .

stop:
	docker stop ${CONTAINER_NAME} || true

run: stop
	docker run --rm -d --name ${CONTAINER_NAME} -p 18080:8080 -v ${HOME}/www:/www ${IMAGE_NAME}

run-node-server: stop
	docker run --rm -d --name ${CONTAINER_NAME} -v ${HOME}/www:/opt/www  -v ${HOME}/music:/opt/www/music  -p 18080:8080 webratio/nodejs-http-server