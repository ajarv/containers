
IMAGE_NAME='m7dock/go-http-server'

build-container:
	docker build -t ${IMAGE_NAME} .

run:
	docker run --rm -d -p 18080:8080 -v ${HOME}/www:/www ${IMAGE_NAME}