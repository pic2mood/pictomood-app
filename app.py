import os
from flask import (
    Flask, render_template, request, url_for, send_from_directory
)
from pictomood.imports import *
from pictomood import config
from pictomood import pictomood

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(
    os.getcwd(),
    'static',
    'uploads'
)


@app.route('/')
def index():
    return render_template(
        'index.html',
        upload_text='DRAG OR CLICK TO UPLOAD.'
    )


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    post_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(post_path)

    get_path = 'http://127.0.0.1:5000/uploads/' + file.filename

    emotion = pictomood.main({
        'single_path': post_path,
        'score': True,
        'model': 'oea',
        'parallel': False,
        'batch': False,
        'montage': False
    })

    return render_template(
        'index.html',
        output_img=get_path,
        emotion_tag=emotion,
        upload_text='DONE.'
    )


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
