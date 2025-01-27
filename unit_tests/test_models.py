import pytest
from app import db, app
from flaskr.models.models import User, UserPasswords

@pytest.fixture
def app_context():
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()

def test_user_model(app_context):
    user = User(username='testuser', password='testpassword', salt='testsalt')
    db.session.add(user)
    db.session.commit()
    assert User.query.count() == 1

def test_user_passwords_model(app_context):
    user = User(username='testuser', password='testpassword', salt='testsalt')
    db.session.add(user)
    db.session.commit()
    password_entry = UserPasswords(user_id=user.id, website='test.com', encrypted_password='encrypted')
    db.session.add(password_entry)
    db.session.commit()
    assert UserPasswords.query.count() == 1