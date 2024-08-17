from flask import Flask
import logging

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py')

    from . import routes
    app.register_blueprint(routes.bp)
    logging.basicConfig(level=logging.DEBUG)
    with app.app_context():
        from . import routes
    return app
