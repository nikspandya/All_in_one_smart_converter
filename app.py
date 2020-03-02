from flask import Flask, render_template, request, send_from_directory, send_file
import os
from PIL import Image
import uuid
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError )

__author__ = 'NIKUL'

app = Flask(__name__)

APP_route = os.path.dirname(os.path.abspath(__file__))

@app.route("/", methods=['GET', 'POST'])
def index():
   return render_template("index.html")

@app.route("/index", methods=['GET', 'POST'])
def upload():
   target = os.path.join(APP_route, 'static/')
   output_format = request.form.get('dropdown')
   if not os.path.isdir(target):
      os.mkdir(target)

   for file in request.files.getlist('file'):
      filename = file.filename
      last_ext = os.path.splitext(filename)[1]
      if last_ext not in ['.jpg', '.png', '.bmp', '.ppm', '.gif', '.tiff', '.pdf']:
         return render_template('error.html')

      else:
          upload.destination = "/".join([target, filename])
          file.save(upload.destination)
          conversion_logic(upload.destination, output_format)
          return render_template('complete.html')

def conversion_logic(file_for_conversion, output_file_format):
    """
    takes the input file & target file extensions
    convert files to target file format
    all pages of pdf file converted to multiple images
    all images are converted to RGB type before saving to avoid image channels conflict
    """
    if file_for_conversion.lower().endswith(('.jpg', '.png', '.bmp', '.ppm', '.gif', '.tiff')):
        Image.open(file_for_conversion).convert('RGB').save(file_for_conversion.split('.')[0] +
        str(uuid.uuid4()) + str(output_file_format.lower()))

    elif file_for_conversion.lower().endswith(('.pdf')):
        images_ppm = convert_from_path(file_for_conversion)
        #images_ppm = convert_from_bytes(open(file_for_conversion, 'rb').read())
        for img in images_ppm:
            img.convert('RGB').save(file_for_conversion.split('.')[0] + str(uuid.uuid4()) +
            str(output_file_format.lower()))


@app.route('/complete.html', methods=['GET', 'POST'])
def downloadFile ():
    path = upload.destination
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
   app.run(debug = True, port=6008)
