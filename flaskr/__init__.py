
import os
import logging
import yaml

from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from flask import Flask, request, jsonify, flash
from werkzeug.utils import secure_filename
from PIL import Image
from configparser import ConfigParser

with open('./config/security.yaml', 'r') as file:
    security_yaml = yaml.load(file,  Loader=yaml.BaseLoader)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_model(weight_path, device):
    model_config = Cfg.load_config_from_name('vgg_transformer')
    model_config['weights'] = weight_path
    model_config['cnn']['pretrained'] = False
    model_config['device'] = device
    model_config['predictor']['beamsearch'] = False
    print(' * Model: load model')
    model = Predictor(model_config)
    print(' * Model: load complete')
    return model


def init_server(custom_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # param config
    if custom_config is not None:
        app.config.from_mapping(custom_config)

    # manual config
    app.config.from_mapping(
        SECRET_KEY="b7HHex1dxdfjxfcxd3x1b!xb4xe6m",
        UPLOAD_FOLDER="./resource",
        MAX_CONTENT_LENGTH=5 * 1024 * 1024,  # EXPLAIN: 5MB
        ROOT_KEY=security_yaml['ROOT_KEY'],
        CURRENT_KEY=security_yaml['CURRENT_KEY']
    )

    # custom loggin
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    return app


def create_app():
    app = init_server()

    print('======================================= MODEL =============================================')
    model = load_model('./models/weights.pth', 'cpu')
    print('======================================= READY =============================================')

    @app.route("/")
    def index():
        return "Hello World!"

    @app.route('/api/predict/captcha', methods=['POST'])
    def upload_to_predict():
        if 'file' not in request.files:
            flash('No file part')
            return "no file upload"

        uploadfile = request.files['file']
        filename = secure_filename(uploadfile.filename)

        if uploadfile and allowed_file(filename):

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploadfile.save(filepath)

            image = Image.open(filepath)
            result = model.predict(img=image)

            os.remove(filepath)
            return result

        return "not allowed: " + filename

    @app.route('/api/micro/current-key', methods=['PUT'])
    def update_current_key():
        key = request.get_json()['key']
        auth = request.headers['auth']

        response = dict({'success': True, 'body': ''})
        if auth == app.config['ROOT_KEY']:
            app.config['CURRENT_KEY'] = key
            response['body'] = 'update success'
        else:
            response['success'] = False
            response['body'] = 'unauthorized'

        return jsonify(response)

    return app
