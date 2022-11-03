from flask import Flask
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from .routes.user_routes import user
from .routes.book_routes import book
from .routes.admin_routes import admin
from .routes.super_admin_routes import superadmin
from .models.user_model import *
import sqlite3
import os, traceback
import bcrypt
from flask_recaptcha import ReCaptcha
from datetime import timedelta
import logging
from flask.logging import default_handler

from flask_session import Session

jwt = JWTManager()
mail = Mail()
recaptcha = ReCaptcha()


def mailSetup():
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "kopickosongml@gmail.com"
    MAIL_PASSWORD = "hEXRsOjFENbBkrcQEZS!"
    SECRET_KEY = 'secretkey'



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    flask_key = '95708a6bdb9148679e01d29975cef0c1'
    app.config['RECAPTCHA_SITE_KEY'] = '6LdYjMwiAAAAABNShyJ2aGa6nFzWi5egcvGIbUUB'
    app.config['RECAPTCHA_SECRET_KEY'] = '6LdYjMwiAAAAAMhJ35HRw06NwAxQO9JZqPpMUqQ5'
    app.config['FLASK_SECRET_KEY'] = flask_key
    app.register_blueprint(user, url_prefix='/apis/user/')
    app.register_blueprint(book, url_prefix='/apis/book/')
    app.register_blueprint(admin, url_prefix='/apis/admin/')
    app.register_blueprint(superadmin, url_prefix='/apis/superadmin/')

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'kopickosongml@gmail.com'
    app.config['MAIL_PASSWORD'] = 'vamjmxizezesorpg'
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
    #log = logging.getLogger('werkzeug')
    #log.setLevel(logging.ERROR)
    #logging.basicConfig(filename='record.log', level=logging.ERROR, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

    jwt.init_app(app)
    mail.init_app(app)
    return app

