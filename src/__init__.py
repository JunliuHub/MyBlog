from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.pagedown import PageDown
from config import config
from flask import Flask

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)

    from .main import main as main_blueprint
    from .site import site as site_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(site_blueprint)

    return app
