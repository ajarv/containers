FROM python:3-alpine

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps

RUN mkdir -p /work

COPY requirements.txt /work/
RUN pip install --no-cache-dir -r /work/requirements.txt

COPY . /work

WORKDIR /work/src

# Expose the Flask port
EXPOSE 5000

CMD [ "python", "./src/s3_event_listener.py" ]