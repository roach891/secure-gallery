from main import app
from database import db
from sqlalchemy.exc import OperationalError

with app.app_context():
    try:
        db.create_all()
        print("Database tables created.")
    except OperationalError:
        print("Tables already exist.")
