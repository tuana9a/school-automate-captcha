
import os
import logging
import io

from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from flask import Flask, request, jsonify, flash
from werkzeug.utils import secure_filename
from PIL import Image
from configparser import ConfigParser

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_model():
    model_config = Cfg.load_config_from_file('./models/config.yml')
    model_config['weights'] = './models/weights.pth'
    model_config['device'] = 'cpu'
    # EXPLAIN: để false vì mình không train
    model_config['cnn']['pretrained'] = False
    model = Predictor(model_config)
    return model


def init_server(custom_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # ensure the instance folder exists
    try:
        instance_path = app.instance_path
        os.makedirs(instance_path)
    except OSError:
        pass
    # param config
    if custom_config is not None:
        app.config.from_mapping(custom_config)

    # manual config
    app.config.from_mapping(
        SECRET_KEY='b7HHex1dxdfjxfcxd3x1b!xb4xe6m',
        MAX_CONTENT_LENGTH=5 * 1024 * 1024,  # EXPLAIN: 5MB
    )

    # custom loggin
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    return app


def create_app():
    app = init_server()
    model = load_model()

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

    return app
