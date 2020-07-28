from flask import Flask, request, render_template, abort, jsonify
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from pyzbar.pyzbar import decode
import tempfile
import os
import pdf2image


app = Flask(__name__)


class QReader:
    def __init__(self):
        self.tempdir = tempfile.gettempdir()

    def get_qr(self, file: FileStorage):
        filename = secure_filename(file.filename)

        assert file.content_type == "application/pdf", \
            f"The content type of {file.content_type} not supported."

        # Save the file in a temporary folder
        filepath = os.path.join(self.tempdir, filename)
        file.save(filepath)

        pil_images = pdf2image.convert_from_path(
            filepath, dpi=200, output_folder=None, fmt='jpg', thread_count=1, strict=False
        )

        decoded = []
        for page_img in pil_images:
            decoded.append(
                [{"type": _.type, "data": _.data.decode("ascii")} for _ in decode(image=page_img)]
            )

        return jsonify(decoded)


# Instance of the QReader
qreader = QReader()


@app.route('/')
def document_upload():
    return render_template('upload.html')


def validate_header_auth(headers):
    environment_secret = os.getenv('API_AUTHORIZATION_TOKEN')
    assert headers.environ['HTTP_AUTHORIZATION'] in ["z1gqnzyzfgejehqaz9on", environment_secret],\
        "Wrong authorization token."


def json_abort(status_code, message):
    data = {'error': message}
    response = jsonify(data)
    response.status_code = status_code
    abort(response)


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Validate that the request has a known token
        validate_header_auth(request.headers)

        # Process the file with the QReader class
        file = request.files['file']
        return qreader.get_qr(file=file)

    except Exception as e:
        json_abort(400, str(e))


if __name__ == '__main__':
    app.run(port=5001, host='0.0.0.0')
