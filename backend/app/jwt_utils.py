import jwt
import uuid
from datetime import datetime, timedelta
from flask import request, jsonify, current_app as app
from functools import wraps

from models import User
from database import db

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    SECRET_KEY = app.config['SECRET_KEY']
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    SECRET_KEY = app.config['SECRET_KEY']
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            bearer = request.headers['Authorization']
            if bearer.startswith('Bearer '):
                token = bearer.split(' ')[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        decoded = decode_access_token(token)
        if 'error' in decoded:
            return jsonify({'error': decoded['error']}), 401

        user = db.session.query(User).filter(User.id == uuid.UUID(decoded['sub'])).first()
        if not user:
            return jsonify({'error': 'Invalid token user'}), 401

        return f(user, *args, **kwargs)
    return decorated
