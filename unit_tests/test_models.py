import pytest
from app import db, app
from flaskr.models.models import User, UserPasswords
from sqlalchemy.exc import IntegrityError

@pytest.fixture
def app_context():
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()

def test_user_model(app_context):
    # create test user
    user = User(username='testuser', password='testpassword', salt='testsalt')
    # add to database session
    db.session.add(user)
    # commit changes to database
    db.session.commit()
    # verify that only one user exists in database
    assert User.query.count() == 1

def test_user_model_invalid_username(app_context):
    # create user with an invalid (NULL) username
    user = User(username=None, password='testpassword', salt='testsalt')
    
    # add to database session
    db.session.add(user)
    
    # expect IntegrityError when committing
    with pytest.raises(IntegrityError):
        db.session.commit()

def test_user_model_duplicate_username(app_context):
    # original user creation
    user1 = User(username='testuser', password='testpassword', salt='testsalt')
    db.session.add(user1)
    db.session.commit()

    # second user with duplicate username
    user2 = User(username='testuser', password='testpassword', salt='testsalt')
    db.session.add(user2)
    
    # expect database to reject duplicate username
    with pytest.raises(IntegrityError):
        db.session.commit()

def test_user_passwords_model(app_context):
    # create test user
    user = User(username='testuser', password='testpassword', salt='testsalt')
    db.session.add(user)
    db.session.commit()

    # create password entry linked to user
    password_entry = UserPasswords(
        user_id=user.id,          # created user's id
        website='test.com',       # test website
        encrypted_password='encrypted'  # test encrypted password
    )
    db.session.add(password_entry)
    db.session.commit()

    # verify password was saved to database
    assert UserPasswords.query.count() == 1

# def test_user_passwords_model_invalid_user_id(app_context):
#     password_entry = UserPasswords(user_id=999, website='test.com', encrypted_password='encrypted')
#     db.session.add(password_entry)
#     with pytest.raises(IntegrityError):
#         db.session.commit()

def test_user_passwords_model_invalid_website(app_context):
    # create test user
    user = User(username='testuser', password='testpassword', salt='testsalt')
    db.session.add(user)
    db.session.commit()

    # create password entry with invalid (NULL) website
    password_entry = UserPasswords(
        user_id=user.id,
        website=None,  # invalid as website entry cant be NULL
        encrypted_password='encrypted'
    )
    db.session.add(password_entry)

    # expect IntegretyError due to NULL website
    with pytest.raises(IntegrityError):
        db.session.commit()