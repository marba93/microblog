from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User 


@app.route('/')
@app.route('/index')
def index():
    user = {'username':'Marcos'}
    posts = [
    	{ 
	    	'tostao': {'username' : ' Pedro'},
	    	'body': 'Has reducido tu ingesta de carbohidratos esta semana'
    	},
    	{ 
	    	'tostao' : {'username': 'Charly'},
	    	'body': ' te ha ganado por 23kcal'
    	}
    	]
    return render_template('index.html', title = 'Fumaos' ,user = user, posts = posts)

@app.route('/login', methods = ['GET','POST'])
def login():
		if current_user.is_authenticated:
			return redirect(url_for('index'))
		form = LoginForm()
		if form.validate_on_submit():
			user = User.query.filter_by(username = form.username.data).first()
			if user is None or not user.check_password(form.password.data):
				flash('Invalid username or password')
				return redirect(url_for('login'))
			login_user(user, remember=form.remember_me.date)
			return redirect(url_for('index'))

			flash('Login requested for user {}, remember_me = {}'.format(
				form.username.data, form.remember_me.data)
				)
			return redirect(url_for('index'))
		return render_template('login.html', title = 'Sign In', form = form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))