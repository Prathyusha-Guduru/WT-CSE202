from digital_wallet import db,login_manager
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