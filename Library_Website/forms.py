from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired,Length

class LoginForm(FlaskForm):
	""" docstring for LoginForm"""
	sapid = StringField('SapID',validators=[DataRequired(),Length(min=9,max=9)])
	password = PasswordField('Password',validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class AddBook(FlaskForm):
	""" docstring for adding books"""
	bookName = StringField('Book Name',validators=[DataRequired(),Length(min=5)])
	addBook = SubmitField('Add Book')