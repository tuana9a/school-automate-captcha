import os
import logging

from flask import Flask


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
    return app
