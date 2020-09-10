FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3.8 python3-pip zbar-tools poppler-utils

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt
