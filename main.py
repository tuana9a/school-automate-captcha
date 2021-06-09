import os
import io
import json
import yaml
import flaskr
import threading

from flask import Flask, request, flash
from werkzeug.utils import secure_filename
from PIL import Image

import services.ModelService as ModelService
import services.AskMasterService as AskMasterService


with open('./config/server.yml') as f:
    config_server = yaml.load(f, Loader=yaml.FullLoader)

with open('./config/model.yml') as f:
    config_model = yaml.load(f, Loader=yaml.FullLoader)


app = flaskr.create_app()
model = ModelService.load_model(
    config_path=config_model['config-path'],
    weights_path=config_model['weights-path'],
    device_type=config_model['device-type']
)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def set_interval(func, sec, delay=True):
    def func_wrapper():
        set_interval(func, sec)
        func()

    if(not delay):
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def ask_worker_address():
    url = config_server['master-address'] + '/api/worker/ask/worker-address'
    data = json.dumps({
        'from':  {
            'name': 'assistant-school-automate-captcha',
            'address': config_server['address']
        },
        'asks': ['assistant-school-automate-captcha']
    })
    AskMasterService.ask_worker_address(url, data)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/predict/captcha', methods=['POST'])
def upload_to_predict():
    if 'file' not in request.files:
        flash('No file part')
        return 'no file upload'

    uploadfile = request.files['file']
    filename = secure_filename(uploadfile.filename)

    if uploadfile and allowed_file(filename):
        try:
            buffers = uploadfile.stream._file.getvalue()
            image = Image.open(io.BytesIO(buffers))
            result = model.predict(img=image)
            return result

        except TypeError:
            return 'Error'

        except ValueError:
            return 'Error'

    return 'not allowed: ' + filename


set_interval(ask_worker_address, 10)
print(' * listen: ' + config_server['address'])
app.run(host='0.0.0.0', port=config_server['port'])
