import pytest
from app import app, db
from flaskr.controller.routes import *

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client  # Test client is yielded herewith 
    with app.app_context():
        db.drop_all()
# happy path
def test_home_page(client):
    #test to check that the home page works
    # make GET request to home page
    response = client.get('/')
    
    # verify 200 response (success)
    assert response.status_code == 200
    
    # verify home page content
    assert b'Home' in response.data

# unhappy path
def test_no_home_page(client):
    # request non-existent page (xyz)
    response = client.get('/xyz')
    
    # verify 404 response (page not found)
    assert response.status_code == 404
    
    # verify the error message
    assert b'404 Not Found' in response.data
