from flask import Flask
from flask import render_template,url_for,flash,redirect,request,session
from forms import LoginForm, AddBook
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from flask_login import login_user,current_user,logout_user,login_required,LoginManager
from flask_login import UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = '15a01884f85e235f933ab44ce5cd1645'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
login_manager = LoginManager(app)

db = SQLAlchemy(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(1))

class User(db.Model,UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	sapid = db.Column(db.String(10),unique=True,nullable=False)
	password = db.Column(db.String(60),nullable=False)
	books = db.relationship('Addbook',backref='author',lazy=True)

	def __repr__(self):
		return f"User('{self.id}','{self.sapid}')"

class Addbook(db.Model):
	date = datetime.now() + timedelta(days=14)
	print(date)
	id = db.Column(db.Integer, primary_key=True)
	bookname = db.Column(db.String(30),nullable=False)
	issuedate = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	duedate = db.Column(db.DateTime,nullable=False,default=date)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

	def __repr__(self):
		return f"Addbook('{self.id}','{self.issuedate}','{self.duedate}','{self.bookname}')"



@app.route("/",methods=['GET','POST'])
@app.route("/home",methods=['GET','POST'])
def home():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(sapid=form.sapid.data).first()
		if user and form.password.data == user.password:
			session['user'] = user.id
			a = User.query.filter_by(id=user.id).first()
			session['books'] = str(a.books)
			login_user(user)
			flash(f'Login Successfull {form.sapid.data}','success')
			return redirect(url_for('account'))
		else:
			flash('Login Unsuccessfull','danger')
	return render_template('login.html',title="Login",form=form)

@app.route("/account")
def account():
	if not(current_user.is_authenticated):
		return redirect(url_for('home'))
	return render_template('account.html',title="Account")

@app.route("/addbook",methods=['GET','POST'])
def addbook():
	if not(current_user.is_authenticated):
		return redirect(url_for('home'))
	form = AddBook()
	if form.validate_on_submit():
		book = Addbook(bookname=form.bookName.data,user_id=session['user'])
		db.session.add(book)
		db.session.commit()
		flash(f'Book added Successfully','success')
		return redirect(url_for('account'))
	return render_template('addbook.html',title="Login",form=form)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

if __name__ == "__main__":
	app.run(debug=True)