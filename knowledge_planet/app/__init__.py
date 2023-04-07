import os
from flask import Flask
from . import api
# from .database import db
from .models import db
# from .models import User



def create_app(config=None):
    #生成核心对象
    app = Flask(__name__)
    if 'FLASK_CONF' in os.environ:
        app.config.from_envvar('FLASK_CONF')
    if config is not None:
        if isinstance(config,dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)
    api.init_app(app)
    db.init_app(app)
    db.create_all(app=app)
    # with app.app_context():
    #     db.create_all()
    return app

