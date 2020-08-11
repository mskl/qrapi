# QRAPI - API for QR code extraction from PDFs 

![Pytest](https://github.com/mskl/qrapi/workflows/Pytest/badge.svg?branch=master) 
Dockerized Flask api with sole purpose of reading QR codes from PDFs. Decoding is done using `pdf2image` and `pyzbar` python libs.

### Structure
Heroku automatically deploys all commits to the master branch where the CI pipeline had passed. The production server is served using gunicorn. When running on Heroku, the app uses a port supplied by Heroku, on localhost the port for testing is 5001. In case you need to debug the app, you can change the `CMD` at the end of Dockerfile to use Flask instead of Gunicorn.

In case you need to add debugging prints into the app, use `app.logger.debug("foo")` where `app` is the flask object.

### Usage
When inside the directory, type
- `make build` to build the image
- `make run` to build and run the image with preset ENV vars and debug
- `make stop` to stop the running image
- `make bash` to access the running container's bash
- `make logs` show the docker logs
- `make rbash` run container only with bash

If you need to see the debug log use
- `docker-compose up`

When in production, do not forget to set the required secret ENV variable:
- `API_AUTHORIZATION_TOKEN`

Sample website is hosted at [http://127.0.0.1/5001](http://127.0.0.1/5001)

### Example
Example response when 3 files are sent, 2 of them with qr codes at the first page.
```json
[
  {
    "content": [
      {
        "data": "5499944158390",
        "page": 0,
        "type": "QRCODE"
      },
      {
        "data": "5499944158390",
        "page": 0,
        "type": "EAN13"
      }
    ],
    "filename": "example.pdf",
    "key": "somefile"
  },
  {
    "content": [],
    "filename": "LSTM_fixed.pdf",
    "key": "file[]"
  },
  {
    "content": [
      {
        "data": "5499944158390",
        "page": 0,
        "type": "QRCODE"
      },
      {
        "data": "5499944158390",
        "page": 0,
        "type": "EAN13"
      }
    ],
    "filename": "example.pdf",
    "key": "file[]"
  }
]
```
