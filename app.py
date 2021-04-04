#!/usr/bin/python3
import os
from flask import Flask, render_template, request, redirect, url_for, json

# Data base lib
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Loging manager lib
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Forms lib
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, Regexp, ValidationError

# boostrap_flask is an maintained fork of flask_bootstrap
from flask_bootstrap import Bootstrap
# import font awesome
from flask_fontawesome import FontAwesome

# JADE lib for data processing (specialy json)
from static.jadeLib.data import Data
from static.jadeLib.dataDocTypeRef import DataDocTypeRef
from static.jadeLib.dataRetentionRef import DataRetentionRef
from static.jadeLib.dataSecurityRef import DataSecurityRef

from static.jadeLib.jadeLogingForm import JadeLogingForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'We4reThe8estTeam'
app.config['BOOTSTRAP_USE_MINIFIED'] = True
bootstrap = Bootstrap(app)
fa = FontAwesome(app)

### DATA BASE PART ###
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////www/app/files/database/login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

### LOGIN SETTINGS ###
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

### INDEX PART ###
@app.route('/')
def index():
    return render_template('pages/index.html')

### LOGIN PART ###
class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15, message='The username need to be between 4 to 15 characters.')])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50), Regexp("^([a-zA-Z0-9_\-\.]+)@eulerhermes.com", message='Must be an @eulerhermes.com email.')])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80, message='The password need to be between 8 to 80 characters.')])

    def validate_username(self, username):
        exist = User.query.filter_by(username=username.data).first()
        if exist:
            raise ValidationError("This account already exist.")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('pages/signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = JadeLogingForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('tables'))
    return render_template('pages/login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

### TABLES PART ###
@app.route('/tables')
@login_required
def tables():
    tableData = Data()
    return render_template('pages/tables.html', user = current_user, tableData = tableData, isEditable = 0)

@app.route('/tableDocTypeRef')
@login_required
def tableDocTypeRef():
    tableData = DataDocTypeRef()
    return render_template('pages/tables.html', user = current_user, tableData = tableData, isEditable = 1)

@app.route('/tableRetentionRef')
@login_required
def tableRetentionRef():
    tableData = DataRetentionRef()
    return render_template('pages/tables.html', user = current_user, tableData = tableData, isEditable = 1)

@app.route('/tableSecurityRef')
@login_required
def tableSecurityRef():
    tableData = DataSecurityRef()
    return render_template('pages/tables.html', user = current_user, tableData = tableData, isEditable = 1)

@app.route('/editTable', methods = ['POST'])
@login_required
def get_post_javascript_data():
    jsdata = request.form.getlist('javascript_data[]')
    if(jsdata.pop(0) == "tableRetentionRef"):
        print("je dois editer pour tableRetentionRef")
        DataRetentionRef.edit(jsdata)
    return "200"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
