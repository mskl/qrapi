from flask import Flask, request, render_template, abort, jsonify
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from werkzeug.exceptions import Unauthorized
from pyzbar.pyzbar import decode
import pdf2image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'

class QReader:
    def __init__(self):
        self.tempdir = "/tmp"

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
        for index, page_img in enumerate(pil_images):
            decoded.extend(
                [
                    {
                        "type": _.type,
                        "data": _.data.decode("utf-8"),
                        "page": index
                    } for _ in decode(image=page_img)
                ]
            )

        return decoded, len(pil_images)


# Instance of the QReader
qreader = QReader()


@app.route('/')
def index():
    # Only show the information index when flask environment is set to development
    flask_env = os.environ.get("FLASK_ENV")
    if flask_env == "development":
        return render_template('index.html', FLASK_ENV=flask_env)
    else:
        abort(404)


def validate_header_auth(headers):
    environment_secret = os.getenv('API_AUTHORIZATION_TOKEN')
    if headers.environ['HTTP_AUTHORIZATION'] != environment_secret:
        raise Unauthorized("Wrong authorization token.")


def json_abort(status_code, message):
    response = jsonify({'error': message})
    response.status_code = status_code
    abort(response)

@app.before_request
def log_request():
    app.logger.info('Content-Type: %s', request.headers['Content-Type'])


@app.route('/echo', methods=['GET'])
def echo():
    try:
        validate_header_auth(request.headers)
        return jsonify({ 'status': 'ok' })
    except Unauthorized as e:
        abort(401)
    except Exception as e:
        abort(500)


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Validate that the request has a known token
        validate_header_auth(request.headers)

        return_list = []

        # Process the all files with the QReader class
        for listname, filelist in request.files.lists():
            for file in filelist:
                content, num_pages = qreader.get_qr(file=file)

                return_list.append({
                    "key": listname,
                    "filename": file.filename,
                    "num_pages": num_pages,
                    "content": content,
                })

        return jsonify(return_list)

    except Unauthorized as e:
        json_abort(401, str(e))
    except Exception as e:
        app.logger.error(e)
        json_abort(500, str(e))


if __name__ == '__main__':
    PORT = os.environ.get("PORT", 5001)
    app.run(port=PORT, host='0.0.0.0')
