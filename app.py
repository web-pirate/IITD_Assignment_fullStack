import os
import pytesseract
from flask import Flask, request, jsonify, render_template
from PIL import Image
import cv2

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get-text', methods=['POST'])
def get_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(image_path)

    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    return jsonify({'text': text})


@app.route('/get-bboxes', methods=['POST'])
def get_bboxes():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    bbox_type = request.form.get('type', 'word')

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(image_path)

    image = cv2.imread(image_path)

    if bbox_type == 'word':
        boxes = pytesseract.image_to_boxes(image)
    elif bbox_type == 'line':
        boxes = pytesseract.image_to_data(
            image, output_type=pytesseract.Output.DICT)
    elif bbox_type == 'paragraph':
        boxes = pytesseract.image_to_data(
            image, output_type=pytesseract.Output.DICT)
    elif bbox_type == 'page':
        boxes = pytesseract.image_to_data(
            image, output_type=pytesseract.Output.DICT)
    else:
        return jsonify({'error': 'Invalid bbox type specified'}), 400

    return jsonify({'boxes': boxes})


if __name__ == '__main__':
    app.run(debug=True)
