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
        user = User(username='testuser', password='testpassword', salt='testsalt')
        db.session.add(user)
        db.session.commit()
        with app.test_request_context('/register', method='POST', data={'username': 'testuser', 'password': 'testpassword'}):
            form = RegisterForm()
            form.validate()
            assert 'username' in form.errors

def test_login_form(client):
    with app.app_context():
        with app.test_request_context('/login', method='POST', data={'username': 'testuser', 'password': 'testpassword'}):
            form = LoginForm()
            form.validate()
            assert not form.errors

def test_password_form(client):
    with app.app_context():
        with app.test_request_context('/dashboard', method='POST', data={'website': 'test.com'}):
            form = PasswordForm()
            form.validate()
            assert not form.errors