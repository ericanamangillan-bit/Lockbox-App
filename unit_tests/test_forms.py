import pytest
from flaskr.service.forms import RegisterForm, LoginForm, PasswordForm
from flaskr.models.models import User
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register_form(client):
    with app.app_context():
        with app.test_request_context('/register', method='POST', data={'username': 'testuser', 'password': 'testpassword'}):
            form = RegisterForm()
            form.validate()
            assert not form.errors

def test_register_form_existing_user(client):
    with app.app_context():
        # create an original user
        user = User(username='testuser', password='testpassword', salt='testsalt')
        db.session.add(user)
        db.session.commit()

        # attempt duplicate registration
        with app.test_request_context('/register', method='POST', data={
            'username': 'testuser',
            'password': 'testpassword'
        }):
            form = RegisterForm()
            form.validate()
            # verify error message
            assert 'username' in form.errors

def test_register_form_invalid_username(client):
    with app.app_context():
        with app.test_request_context('/register', method='POST', data={
            'username': 'a',  # invalid as too short
            'password': 'testpassword'
        }):
            form = RegisterForm()
            form.validate()
            assert 'username' in form.errors

def test_register_form_invalid_password(client):
    with app.app_context():
        with app.test_request_context('/register', method='POST', data={
            'username': 'testuser',
            'password': 'short'  # invalid as too short
        }):
            form = RegisterForm()
            form.validate()
            assert 'password' in form.errors

def test_login_form(client):
    with app.app_context():
        # test login with valid credentials
        with app.test_request_context('/login', method='POST', data={
            'username': 'testuser',
            'password': 'testpassword'
        }):
            form = LoginForm()
            form.validate()
            # verify no validation errorrs
            assert not form.errors

def test_login_form_invalid_username(client):
    with app.app_context():
        with app.test_request_context('/login', method='POST', data={
            'username': 'a',  # invalid as too short
            'password': 'testpassword'
        }):
            form = LoginForm()
            form.validate()
            assert 'username' in form.errors

def test_login_form_invalid_password(client):
    with app.app_context():
        with app.test_request_context('/login', method='POST', data={
            'username': 'testuser',
            'password': 'short'  # invalid as to short
        }):
            form = LoginForm()
            form.validate()
            assert 'password' in form.errors

def test_password_form(client):
    with app.app_context():
        with app.test_request_context('/dashboard', method='POST', data={'website': 'test.com'}):
            form = PasswordForm()
            form.validate()
            assert not form.errors

def test_password_form_invalid_website(client):
    with app.app_context():
        with app.test_request_context('/dashboard', method='POST', data={
            'website': 'tes'  # invalid as too short
        }):
            form = PasswordForm()
            form.validate()
            assert 'website' in form.errors