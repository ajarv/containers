
IMAGE_NAME='m7dock/go-http-server'
build-container:
	docker build -f ${IMAGE_NAME} .

run:
	docker run --rm -d -p 18080:8080 -v $(static-dir):/www ${IMAGE_NAME}