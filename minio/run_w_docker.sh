#!/bin/bash


docker run -d \
  -p 9000:9000 \
  -p 9001:9001 \
  -v /mnt/ssd/data:/data \
  -e "MINIO_ROOT_USER=kalpa" \
  -e "MINIO_ROOT_PASSWORD=rekongpeo" \
  quay.io/minio/minio server /data --console-address "0.0.0.0:9001"
