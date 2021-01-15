from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg


def load(weight_path, device):
    model_config = Cfg.load_config_from_name('vgg_transformer')
    model_config['weights'] = weight_path
    model_config['cnn']['pretrained'] = False
    model_config['device'] = device
    model_config['predictor']['beamsearch'] = False
    model = Predictor(model_config)
    return model
