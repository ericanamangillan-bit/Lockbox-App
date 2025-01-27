import pytest
from app import app, db
from flaskr.models.models import User
from flaskr.service.services import custom_hash

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

def test_register(client):
    with app.app_context():
        response = client.post('/register', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)
        assert response.status_code == 200
        assert b'Login' in response.data

def test_login(client):
    with app.app_context():
        salt = 'testsalt'
        hashed_password = custom_hash('testpassword', salt)
        user = User(username='testuser', password=hashed_password, salt=salt)
        db.session.add(user)
        db.session.commit()
        response = client.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)
        assert response.status_code == 200
        assert b'Dashboard' in response.data

def test_login_invalid_password(client):
    with app.app_context():
        salt = 'testsalt'
        hashed_password = custom_hash('testpassword', salt)
        user = User(username='testuser', password=hashed_password, salt=salt)
        db.session.add(user)
        db.session.commit()
        
        with client.session_transaction() as session:
            response = client.post('/login', data=dict(
                username='testuser',
                password='wrongpassword'
            ), follow_redirects=True)
            
        assert response.status_code == 200
        assert b'Invalid username or password' in response.data