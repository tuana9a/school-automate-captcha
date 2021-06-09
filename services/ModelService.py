from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg


def load_model(config_path, weights_path, device_type):
    model_config = Cfg.load_config_from_file(config_path)
    model_config['weights'] = weights_path
    model_config['device'] = device_type
    # EXPLAIN: để false vì mình không train
    model_config['cnn']['pretrained'] = False
    model = Predictor(model_config)
    return model
