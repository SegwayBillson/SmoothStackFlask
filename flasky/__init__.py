import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app  = Flask(__name__)  # Decorator!

'''
Main flasky package. Handles initialization
'''

app.config['SECRET_KEY'] = '829c714a59906af44da4289266ccafed'   # Random string generated by secret module
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'     # Creates database in current directory
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('SMOOTH_EMAIL')
app.config['MAIL_PASSWORD'] = os.getenv('SMOOTH_PASS')
mail = Mail(app)

from flasky import routes