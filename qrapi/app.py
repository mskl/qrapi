from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from pyzbar.pyzbar import decode
import tempfile
import os
import pdf2image
from PIL import Image
import time


app = Flask(__name__)


class QReader:
    def __init__(self):
        self.tempdir = tempfile.gettempdir()

    @classmethod
    def get_qr(cls, file):
        pass


@app.route('/')
def hello_world():
    return """
        <a href="/send_document">upload a pdf</a>
    """


@app.route('/send_document')
def send_document():
    return render_template('upload.html')


@app.route('/pdfupload', methods=['GET', 'POST'])
def upload_file():
    tempdir = tempfile.gettempdir()

    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        savepath = os.path.join(tempdir, filename)

        file.save(savepath)

        pil_images = pdf2image.convert_from_path(
            savepath, dpi=200, output_folder=None, fmt='jpg', thread_count=1, strict=False
        )

        decoded = {}

        for page_num, page_img in enumerate(pil_images):
            decoded_list = decode(image=page_img)
            decoded[page_num] = [{"type": _.type, "data": _.data.decode("ascii")} for _ in decoded_list]

        return decoded


if __name__ == '__main__':
    app.run(debug=True)
