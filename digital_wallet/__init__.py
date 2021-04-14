from operator import imod
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


from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer,primary_key = True)
	profile_image = db.Column(db.String(20),nullable = False,default = 'default.jpg')
	email = db.Column(db.String(64),unique = True,index = True)
	username = db.Column(db.String(64),unique = True,index = True)
	password_hash = db.Column(db.String(128))
	amount = db.Column(db.Integer,default = 0)

	def __init__(self,email,username,password):
		self.email = email
		self.username = username
		self.password_hash = generate_password_hash(password)
	def check_password(self,password):
		return check_password_hash(self.password_hash,password)

	def add_amount(self,amount):
		self.amount = amount

	def __repr__(self):
		return f"Username is {self.username}"