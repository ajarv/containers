
IMAGE_NAME='m7dock/go-ran'
CONTAINER_NAME='file-server-ran'

build-container:
	docker build -t ${IMAGE_NAME} .

stop:
	docker stop ${CONTAINER_NAME} || true

run: stop
	docker run --rm -d --name ${CONTAINER_NAME} -p 18080:8080 -v ${HOME}/www:/www ${IMAGE_NAME} \
	-r /www -cors=true -l 
 