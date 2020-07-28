from flask import Flask, request, render_template, abort
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
        try:
            filename = secure_filename(file.filename)

            assert file.content_type == "application/pdf", \
                f"The content type of {file.content_type} not supported."

            # Save the file in a temporary folder
            filepath = os.path.join(self.tempdir, filename)
            file.save(filepath)

            pil_images = pdf2image.convert_from_path(
                filepath, dpi=200, output_folder=None, fmt='jpg', thread_count=1, strict=False
            )

            decoded = {}
            for page_num, page_img in enumerate(pil_images):
                decoded_list = decode(image=page_img)
                decoded[page_num] = [{"type": _.type, "data": _.data.decode("ascii")} for _ in decoded_list]

            return decoded
        except Exception as e:
            abort(400, str(e))


# Instance of the QReader
qreader = QReader()


@app.route('/')
def document_upload():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    return qreader.get_qr(file=file)


if __name__ == '__main__':
    app.run(debug=False, port=5001, host='0.0.0.0')
