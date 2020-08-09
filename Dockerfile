FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3.8 python3-pip zbar-tools poppler-utils

# Code is copied on build. In development, we mount a local folder over a copied one.
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY qrapi/ /app/

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]