
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_login.utils import login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'izzasecret'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
