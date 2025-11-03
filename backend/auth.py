# auth.py
import jwt
import os
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps

def generate_token(user_id):
    """
    Generate a JWT token for authenticated users
    """
    try:
        payload = {
            'sub': user_id,
            'username': 'quantum_miner',
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        # Use your secret key from environment variables
        secret_key = os.getenv('SECRET_KEY', 'pi-forge-kris-olofson-2024')
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token
    except Exception as e:
        print(f"Token generation error: {e}")
        return None

def token_required(f):
    """
    Decorator to protect routes that require authentication
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Decode and verify the token
            secret_key = os.getenv('SECRET_KEY', 'pi-forge-kris-olofson-2024')
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            current_user = {
                'sub': payload['sub'],
                'username': payload['username']
            }
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token is invalid'}), 401
        except Exception as e:
            return jsonify({'error': 'Token verification failed'}), 401
        
        # Pass the current user to the protected route
        return f(current_user, *args, **kwargs)
    
    return decorated
