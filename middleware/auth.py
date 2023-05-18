import traceback
from functools import wraps

from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidTokenError
)
from flask import request

from controller.token import TokenController
from controller.role_permission import RolePermissionController

token_controller = TokenController()
role_permission_controller = RolePermissionController()

def permission_required(required_permission:str) -> dict:

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                role_id = request.user.get("role_id")
                is_has_permission = role_permission_controller.has_permission(
                    role_id,
                    required_permission
                )
                if not is_has_permission:
                    return {"message":"Forbidden"}, 403
                
                return func(*args, **kwargs)
            except:
                traceback.print_exc()
                return {"message":"Bad request"}, 400
            
        return wrapper
    return decorator

def token_required(func) -> dict: 
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            auth = request.headers.get("Authorization")
            if not auth:
                return {"message":"Unauthorized"}, 401
            
            jwt_access_token = auth.split(" ")[1]
            
            payload = token_controller.decode_access_token(jwt_access_token)

            is_token_has_been_revoked = token_controller.has_been_revoked(jwt_access_token)
            if is_token_has_been_revoked:
                return {"message":"Revoked token"}, 400

            # extend data to the request object
            request.user={
                "id":payload.get("id"),
                "name":payload.get("name"),
                "role_id":payload.get("role_id")
            }
            
            return func(*args, **kwargs)
        
        except ExpiredSignatureError:
            return {"message":"Expired token"}, 400
        except InvalidTokenError:
            traceback.print_exc()
            return {"message":"Invalid token"}, 400
        except:
            traceback.print_exc()
            return {"message":"Bad request"}, 400
    return wrapper


