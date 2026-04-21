from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database_changed.db")}'
app.config['SECRET_KEY'] = "secret_key"
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Add this line
login_manager.login_message = 'Please log in to access this page.'  # Add this line

@login_manager.user_loader
def load_user(user_id):
    from flaskr.models.models import User
    return User.query.get(int(user_id))

from flaskr.controller.routes import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)