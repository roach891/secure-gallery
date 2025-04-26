from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
import bcrypt

from models import User
from database import db
from jwt_utils import create_access_token

auth_bp = Blueprint('auth', __name__)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({'error': 'Username and password cannot be empty.'}), 400

    if len(username) < 4:
        return jsonify({'error': 'Username must be at least 4 characters long.'}), 400

    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters long.'}), 400

    db_user = db.session.query(User).filter(User.username == username).first()
    if db_user:
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = hash_password(password)
    db_user = User(username=username, password=hashed_password)
    db.session.add(db_user)
    db.session.commit()
    db.session.close()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({'error': 'Username and password cannot be empty.'}), 400

    if len(username) < 4:
        return jsonify({'error': 'Username must be at least 4 characters long.'}), 400

    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters long.'}), 400

    db_user = db.session.query(User).filter(User.username == username).first()
    if not db_user or not verify_password(password, db_user.password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(data={"sub": str(db_user.id), "username": db_user.username})
    db.session.close()

    return jsonify({"access_token": access_token, "token_type": "bearer"})
