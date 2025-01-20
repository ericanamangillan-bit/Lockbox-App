from flask import Flask, render_template, url_for, request, redirect, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
import random
import string
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database_changed.db")}'
app.config['SECRET_KEY'] = "secret_key"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class UserPasswords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    website = db.Column(db.String(150), nullable=False)
    encrypted_password = db.Column(db.String(150), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

class PasswordForm(FlaskForm):
    website = StringField(validators=[
                          InputRequired(), Length(min=4, max=150)], render_kw={"placeholder": "Website"})
    submit = SubmitField('Generate Password')

def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def custom_encrypt(text, shift=3):
    encrypted = ''.join(chr((ord(char) + shift - 32) % 95 + 32) for char in text)
    return encrypted

def custom_decrypt(text, shift=3):
    decrypted = ''.join(chr((ord(char) - shift - 32) % 95 + 32) for char in text)
    return decrypted

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = PasswordForm()
    if form.validate_on_submit():
        website = form.website.data
        generated_password = generate_strong_password()
        encrypted_password = custom_encrypt(generated_password)
        new_password_entry = UserPasswords(user_id=current_user.id, website=website, encrypted_password=encrypted_password)
        db.session.add(new_password_entry)
        db.session.commit()
        flash(f'Generated password for {website}: {generated_password}', 'success')
    user_passwords = UserPasswords.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', form=form, user_passwords=user_passwords)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and custom_decrypt(user.password) == form.password.data:  # Compare decrypted password
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        encrypted_password = custom_encrypt(form.password.data)  # Encrypt the password
        new_user = User(username=form.username.data, password=encrypted_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/decrypt_password/<int:password_id>')
@login_required
def decrypt_password(password_id):
    password_entry = UserPasswords.query.get_or_404(password_id)
    if password_entry.user_id != current_user.id:
        abort(403)
    decrypted_password = custom_decrypt(password_entry.encrypted_password)
    flash(f'Decrypted password for {password_entry.website}: {decrypted_password}', 'info')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)