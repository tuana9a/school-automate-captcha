# import matplotlib.pyplot as plt
from PIL import Image

from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg

def load_model(weith_path, device):
    config = Cfg.load_config_from_name('vgg_transformer')
    config['weights'] = weith_path
    config['cnn']['pretrained'] = False
    config['device'] = device
    config['predictor']['beamsearch'] = False
    model = Predictor(config)
    return model 

model = load_model('models/weights.pth', 'cpu')

img_path = 'models/validate/test5.png'
img = Image.open(img_path)
result = model.predict(img)
print(result)
