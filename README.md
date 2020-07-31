# qRAPi
REST API to render PDF pages and extract QR codes from them.

### Usage
When inside the directory, type
- `make build` to build the image
- `make run-dev` to run the image with preset ENV vars and debug
    - `make run` to run the image without preset ENV vars
- `make stop` to stop the running image
- `make bash` to access the running container's bash

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
    "name": "file"
  },
  {
    "content": [],
    "name": "file without qr"
  }
]
```