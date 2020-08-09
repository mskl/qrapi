# qRAPi
REST API to render PDF pages and extract QR codes from them.

### Usage
When inside the directory, type
- `make build` to build the image
- `make run` to run the image with preset ENV vars and debug
- `make stop` to stop the running image
- `make bash` to access the running container's bash

If you need to see the debug log use
- `docker-compose up`

When in production, do not forget to set the required secrets:
- `API_AUTHORIZATION_TOKEN`

Sample website is hosted at [127.0.0.1/5001](127.0.0.1/5001)

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