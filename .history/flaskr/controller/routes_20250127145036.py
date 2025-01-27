from flask import render_template, url_for, request, redirect, flash, jsonify, abort
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db
from flaskr.models.models import User, UserPasswords
from flaskr.service.services import generate_strong_password, custom_encrypt, custom_decrypt, custom_hash
from flaskr.service.forms import RegisterForm, LoginForm, PasswordForm
import random, string

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required  # Ensure this decorator is present
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
        
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
        if user and custom_hash(form.password.data, user.salt) == user.password:
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        hashed_password = custom_hash(form.password.data, salt)  # Hash the password
        new_user = User(username=form.username.data, password=hashed_password, salt=salt)
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
@login_required  # Add login protection
def decrypt_password(password_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
        
    password_entry = UserPasswords.query.get_or_404(password_id)
    if password_entry.user_id != current_user.id:
        abort(403)
    decrypted_password = custom_decrypt(password_entry.encrypted_password)
    flash(f'Decrypted password for {password_entry.website}: {decrypted_password}', 'info')
    return redirect(url_for('dashboard'))

@app.route('/get_passwords', methods=['GET'])
@login_required  # Add login protection
def get_passwords():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_passwords = UserPasswords.query.filter_by(user_id=current_user.id).all()
    passwords = [{'website': p.website, 'password': custom_decrypt(p.encrypted_password)} for p in user_passwords]
    return jsonify(passwords)