# FROM python:3.7-alpine

FROM python:3.7.2-slim


ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# RUN apt-get install build-essential libssl-dev libffi-dev python3-dev python-dev
# RUN apt-get build-dep python-imaging
# RUN apt-get install libjpeg62 libjpeg62-dev
# RUN pip install PIL
# RUN apk add --no-cache jpeg-dev zlib-dev
# RUN apk add --no-cache --virtual .build-deps build-base linux-headers
# RUN pip3 install django-rest-knox
RUN pip3 install -r /requirements.txt


WORKDIR /app
COPY ./tees_project /app

# RUN adduser -D user
# USER user
# RUN pip3 install virtualenv --user
# RUN python3 - virtualenv /app/env
# RUN source /app/env/bin/activate
