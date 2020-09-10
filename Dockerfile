FROM skalimat/qrapi:latest

# Code is copied on build. In development, we mount a local folder over a copied one.
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY qrapi/ /app/

# gunicorn config is located in /misc folder
COPY misc/gunicorn_config.py /misc/

# Use the following in development when debugging is needed
# CMD ["python3", "app.py"]

# Use the following in production
CMD ["/usr/local/bin/gunicorn", "-c", "/misc/gunicorn_config.py", "app:app"]
