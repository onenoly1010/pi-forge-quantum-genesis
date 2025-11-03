import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app
from python_decouple import config

def generate_token(user_id, username):
    """Generate JWT token for authenticated user"""
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id,
            'username': username
        }
        return jwt.encode(
            payload,
            config('SECRET_KEY', default='fallback-secret-key'),
            algorithm='HS256'
        )
    except Exception as e:
        raise e

def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(
            token,
            config('SECRET_KEY', default='fallback-secret-key'),
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception('Token expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')

def token_required(f):
    """Decorator to protect routes with JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid authorization header'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            current_user = verify_token(token)
        except Exception as e:
            return jsonify({'error': str(e)}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated
