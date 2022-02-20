from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import logging, logging.handlers
log_file_name = 'flaskblog/logs/log.txt'

def Logger():
    logger = logging.getLogger('logs')
    logger.setLevel(logging.DEBUG)
    format = logging.Formatter('[%(asctime)s  %(levelname)s]  %(message)s')
    filehandler = logging.handlers.RotatingFileHandler(filename=log_file_name, backupCount=2)
    filehandler.setLevel(logging.DEBUG)
    filehandler.setFormatter(format)
    logger.addHandler(filehandler)
    return logger


logger = Logger()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('CONNECTION_STRING')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
mail = Mail(app)
from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main
from flaskblog.errors.errorshandlers import errors
from flaskblog.comment.routes import comment
from flaskblog.reply.routes import reply
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)
app.register_blueprint(comment)
app.register_blueprint(reply)