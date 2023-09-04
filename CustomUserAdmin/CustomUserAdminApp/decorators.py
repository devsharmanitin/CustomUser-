import jwt
from django.contrib import messages
from django.shortcuts import redirect 

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token , 'secret' , algorithms='HS256')
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None


def validate_jwt_token(view_func):
    def wrapper(request , *args, **kwargs):
        jwt_token = request.session.get('jwt_token')
        
        if jwt_token:
            payload = decode_jwt_token(jwt_token)
            if payload and payload.get('email'):
                return view_func(request , *args, **kwargs)
        messages.warning(request , 'You are Not Authorized to access that Content')
        return redirect('UserAccountLoginView')
    return wrapper