
import os
import yaml
import model
import logging

from flask import Flask, request
from werkzeug.utils import secure_filename
from PIL import Image


with open('config.yaml', 'r') as file:
    config_yaml = yaml.load(file,  Loader=yaml.BaseLoader)
UPLOAD_FOLDER = config_yaml['server']['upload']

app = Flask(__name__)
app.config['MAX_CONTENT_PATH'] = 100000
model = model.load(config_yaml['model']['path'], 'cpu')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/api/predict/captcha', methods=['POST'])
def upload_to_predict():
    uploadfile = request.files['file']
    filename = secure_filename(uploadfile.filename)

    filepath = './captcha/' + filename
    uploadfile.save(os.path.join(UPLOAD_FOLDER, filename))

    result = model.predict(Image.open(filepath))
    os.remove(filepath)

    return result


app.run(port=config_yaml['server']['port'], debug=True)
