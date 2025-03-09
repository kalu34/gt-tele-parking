import jwt
from django.conf import settings
from datetime import datetime, timedelta

def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,  
        'exp': datetime.utcnow() + timedelta(hours=getattr(settings, 'JWT_EXPIRATION_HOURS', 24)),
        'iat': datetime.utcnow()
    }

    token = jwt.encode(payload, getattr(settings, 'JWT_SECRET_KEY'), algorithm=getattr(settings, 'JWT_ALGORITHM', 'HS256')) # Default HS256 if not in settings
    print(token)
    return token

def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, getattr(settings, 'JWT_SECRET_KEY'), algorithms=[getattr(settings, 'JWT_ALGORITHM', 'HS256')])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Token is invalid
    except Exception as e:
        print(f"JWT verification error: {e}")  # Log the error for debugging
        return None  # Some other error occurred