# filepath: /C:/Users/Stella/lockbox/lockbox2/init_db.py
from app import app, db

with app.app_context():
    db.create_all()
    print("Database tables created.")

