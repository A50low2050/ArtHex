import os
from flask import Flask
from flask_login import LoginManager

from .database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    with app.test_request_context():
        from app.firstmodules.models import Users
        db.create_all()

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'alert alert-dark'

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    from app.firstmodules.controllers import module as module_blueprint
    from app.firstmodules.auth import auth as auth_blueprint
    from app.firstmodules.uploads import uploads as uploads_blueprint
    from app.firstmodules.removes import removes as removes_blueprint
    from app.firstmodules.updates import updates as updates_blueprint

    app.register_blueprint(module_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(uploads_blueprint)
    app.register_blueprint(removes_blueprint)
    app.register_blueprint(updates_blueprint)

    return app


def get_app():
    app = Flask(__name__)
    return app
