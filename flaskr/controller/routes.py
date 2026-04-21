from flask import render_template, url_for, request, redirect, flash, jsonify, abort
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db
from flaskr.models.models import User, UserPasswords
from flaskr.service.services import generate_strong_password, custom_encrypt, custom_decrypt, custom_hash
from flaskr.service.forms import RegisterForm, LoginForm, PasswordForm
import random, string

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required  # ensures only authenticated users can acess the dashboard
def dashboard():
    if not current_user.is_authenticated: 
        return redirect(url_for('login'))
        # redirect back to the login page if the user is not authenticated

    form = PasswordForm()
    if form.validate_on_submit():
        website = form.website.data
        generated_password = generate_strong_password()
        encrypted_password = custom_encrypt(generated_password)
        # generate and encrypt a new password
        new_password_entry = UserPasswords(user_id=current_user.id, website=website, encrypted_password=encrypted_password)
        # create a new password entry in the database
        db.session.add(new_password_entry)
        db.session.commit()
        # commit the changes to the database
        flash(f'Generated password for {website}: {generated_password}', 'success')
        # shows a message to the user that the password was generated successsfully along with the password
    user_passwords = UserPasswords.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', form=form, user_passwords=user_passwords)
    # shows all of the user's passwords on the dashboard

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and custom_hash(form.password.data, user.salt) == user.password:
            login_user(user)
            return redirect(url_for('dashboard'))
        # check if the user exists and the password is correct
        flash('Invalid username or password')
        # show an error message if the username or password is incorrect
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        # generate a random salt for use during password hashing
        hashed_password = custom_hash(form.password.data, salt) 
        # hashes the password
        new_user = User(username=form.username.data, password=hashed_password, salt=salt)
        # create a new user object in the database
        db.session.add(new_user)
        db.session.commit()
        # commit the changes to the database
        return redirect(url_for('login'))
        # redirect the user to the login page
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
# ensures only authenticated users can logout
def logout():
    logout_user()
    # logs the user out
    return redirect(url_for('home'))
    # sends the user back to the home page

@app.route('/decrypt_password/<int:password_id>')
@login_required  
# ensures the user is logged in
def decrypt_password(password_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    # redirect the user to ther login page if they are not authenticated
        
    password_entry = UserPasswords.query.get_or_404(password_id)
    # retrieve the password entry from the database 
    if password_entry.user_id != current_user.id:
        abort(403)
    # return a 403 error if the user is not authorised to view the password
    decrypted_password = custom_decrypt(password_entry.encrypted_password)
    flash(f'Decrypted password for {password_entry.website}: {decrypted_password}', 'info')
    # show the decrypted password to the user
    return redirect(url_for('dashboard'))
    # send the user back to the dashboard

@app.route('/get_passwords', methods=['GET'])
@login_required 
# ensures the user is logged in
def get_passwords():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized'}), 401
    # return a 401 error if the user is not authenticated
    
    user_passwords = UserPasswords.query.filter_by(user_id=current_user.id).all()
    # retrieve all the user's password entries from the database
    passwords = [{'website': p.website, 'password': custom_decrypt(p.encrypted_password)} for p in user_passwords]
    # decrypt the passwords and store them in a list
    return jsonify(passwords)

# def register_routes(app):
#     app.add_url_rule('/', 'homepage', home)
# # register the home route
