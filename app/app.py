from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

login_manager = LoginManager()
login_manager.login_view = "auth_blueprint.login"
login_manager.login_message = "please login to access this page"
login_manager.login_message_category = "error"

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialization
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    #routes
    from .auth.auth_blueprint import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .admin.admin_blueprint import admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/administrator')

    return app
