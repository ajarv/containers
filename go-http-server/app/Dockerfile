# build stage
FROM golang:alpine AS build-env
RUN apk --no-cache add build-base git gcc
RUN go get -u github.com/m3ng9i/ran

# final stage
FROM alpine 
WORKDIR /app
COPY --from=build-env /go/bin/ran /app/ran
ENTRYPOINT ./ran