FROM python:3.10.12-alpine

RUN apk update && apk add --no-cache --virtual bash gcc musl-dev linux-headers jpeg-dev zlib-dev mariadb-dev libffi-dev

COPY ./python_publisher/ /var/www/python_publisher
COPY docker/python_publisher/requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "mqtt_publisher.py"]
