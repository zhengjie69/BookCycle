from flask import Flask
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from .routes.user_routes import user
from .routes.book_routes import book
from .routes.admin_routes import admin
from .routes.super_admin_routes import superadmin
from .models.user_model import *
from .models.key_model import *
import os, traceback
from flask_recaptcha import ReCaptcha
from datetime import timedelta
import logging
from flask.logging import default_handler

from flask_session import Session

jwt = JWTManager()
mail = Mail()
recaptcha = ReCaptcha()



def create_app(test_config=None):
    # create and configure the app
    keyModel = key()
    app = Flask(__name__, instance_relative_config=True)
    

    app.register_blueprint(user, url_prefix='/apis/user/')
    app.register_blueprint(book, url_prefix='/apis/book/')
    app.register_blueprint(admin, url_prefix='/apis/admin/')
    app.register_blueprint(superadmin, url_prefix='/apis/superadmin/')

    app.config['RECAPTCHA_SECRET_KEY'] = keyModel.get_key("RECAPTCHA_SECRET_KEY")
    app.config['FLASK_SECRET_KEY'] = keyModel.get_key("FLASK_SECRET_KEY")

    app.config['MAIL_SERVER'] = keyModel.get_key("MAIL_SERVER")
    app.config['MAIL_PORT'] = int(keyModel.get_key("MAIL_PORT"))
    app.config['MAIL_USERNAME'] = keyModel.get_key("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = keyModel.get_key("MAIL_PASSWORD")
    app.config['MAIL_USE_SSL'] = True

    userModel = User()
    app.config['SECRET_KEY'] = userModel.get_key()


    UPLOAD_FOLDER = os.path.join('static', 'BookImages')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    recaptcha.init_app(app)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.permanent_session_lifetime = timedelta(minutes=30)
    Session(app)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    logging.basicConfig(filename='record.log', level=logging.ERROR, format=f'%(asctime)s - %(levelname)s - %(name)s - %(threadName)s : %(message)s')

    jwt.init_app(app)
    mail.init_app(app)
    return app

