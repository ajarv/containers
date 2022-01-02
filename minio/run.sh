#!/bin/bash


export MINIO_ACCESS_KEY=brightangel
export MINIO_SECRET_KEY=northkaibab
export DATA_DIR=/var/lib/data/minio-data
nohup minio server ${DATA_DIR} >> /tmp/minio.log &
