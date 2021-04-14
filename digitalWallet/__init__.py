#########################################
### importing 3rd party libraries   #####
#########################################


from operator import imod
from flask import Flask,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_login.utils import login_required
from flask_wtf import FlaskForm
from flask_wtf.csrf import _FlaskFormCSRF
from wtforms import StringField,PasswordField,SubmitField
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from flask import render_template
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash



#########################################
################## CONFIG    ############
#########################################


app = Flask(__name__)
app.config['SECRET_KEY'] = 'izzasecret'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)





#########################################
################## DB MODELS ############
#########################################

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer,primary_key = True)
	profile_image = db.Column(db.String(20),nullable = False,default = 'default.jpg')
	email = db.Column(db.String(64),unique = True,index = True)
	username = db.Column(db.String(64),unique = True,index = True)
	password_hash = db.Column(db.String(128))
	amount = db.Column(db.Integer,default = 0)

	def __init__(self,email,username,password,amount):
		self.email = email
		self.username = username
		self.password_hash = generate_password_hash(password)
		self.amount = amount
	def check_password(self,password):
		return check_password_hash(self.password_hash,password)

	def add_amount(self,amount):
		self.amount = amount

	def __repr__(self):
		return f"Username is {self.username}"


#########################################
################## FORMS ################
#########################################

class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	username = StringField('Username',validators=[DataRequired()])
	password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message='Passwords must match')])
	pass_confirm = PasswordField('Conifirm Password',validators=[DataRequired()])
	amount = IntegerField('How much amount do ou want to add',validators=[DataRequired()])
	submit = SubmitField('Register')

	def check_email(self,field):
		if User.query.filter_by(email = field.data).first():
			raise ValidationError('Email has been registered already ')
	
	def check_username(self,field):
		if User.query.filter_by(username = field.data).first():
			raise ValidationError('Username has been registered already ')

	
class UpdateUserForm(FlaskForm):

	
	email = StringField('Email',validators=[DataRequired(),Email()])
	username = StringField('Username',validators=[DataRequired()])
	picture = FileField('Update Profile Picture',validators= [FileAllowed(['png','jpg'])])
	amount = IntegerField('Updated amount',validators=[DataRequired()])
	submit = SubmitField('Update')
	def check_email(self,field):
		if User.query.filter_by(email = field.data).first():
			raise ValidationError('Email has been registered already ')
	
	def check_username(self,field):
		if User.query.filter_by(username = field.data).first():
			raise ValidationError('Username has been registered already ')


#########################################
################## VIEWS ################
#########################################

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register',methods = ['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
			user = User(email = form.email.data,username=form.username.data,password=form.password.data,amount = form.amount.data)
			db.session.add(user)
			db.session.commit()
			flash("Thanks for registration")
			return redirect(url_for('login'))
	return render_template('register.html',form = form)

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/add_money')
def add_money():
	return render_template('add_money.html')

@app.route('/transaction')
def transaction():
	return render_template('transaction.html')

