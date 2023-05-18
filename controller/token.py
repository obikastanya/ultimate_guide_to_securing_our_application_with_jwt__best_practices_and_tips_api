import hashlib
import traceback
from datetime import datetime, timedelta

import jwt

import config

from model.revoked_token import RevokedToken

class TokenController:
    def __init__(self):
        self.revoked_token = RevokedToken()

    def create_access_token(self, payload: dict):
        # will expired after an hours
        return self._create_token(payload, config.ACCESS_TOKEN_SECRET_KEY, 60)
        
    def create_refresh_token(self, payload: dict):
        # will expired after 3 hours
        return self._create_token(payload, config.REFRESH_TOKEN_SECRET_KEY, 180)
    
    def decode_access_token(self, access_token: str):
        return self._decode_token(access_token, config.ACCESS_TOKEN_SECRET_KEY)
         
    def decode_refresh_token(self, refresh_token: str):
        return self._decode_token(refresh_token, config.REFRESH_TOKEN_SECRET_KEY)
    
    def has_been_revoked(self, access_token):
        access_token = self._hash_token(access_token)
        is_token_has_been_revoked = self.revoked_token.has_been_revoked(access_token)
        if is_token_has_been_revoked:
            return True
        return False
        
    
    def clear_revoked_token(self):
        try:
            max_expiration = datetime.now()
            self.revoked_token.clear_revoked_token(max_expiration)
            return {"message":"Success"}, 200
        except:
            traceback.print_exc()
            return {"message":"Internal server error"}, 500
        
    def revoke_access_token(self, access_token: str):
        try:
            payload = self.decode_access_token(access_token)
            expired_at = payload.get("exp")
            expired_at = datetime.fromtimestamp(expired_at)

            access_token = self._hash_token(access_token)
            record_inserted =self.revoked_token.revoke_token(access_token,expired_at)
            if not record_inserted:
                return {"message":"Failed to revoke token "}, 500    
            
            return {"message":"Success"}, 200
        except:
            traceback.print_exc()
            return {"message":"Internal server error"}, 500
   
    def refresh_token(self, access_token: str, refresh_token: str):
        try:
            is_token_has_been_revoked = self.revoked_token.has_been_revoked(access_token)
            if is_token_has_been_revoked:
                return {"message":"Token has been revoked"}, 400
            
            is_valid_access_token, error_message = self._safely_decode_access_token(access_token)
            if not is_valid_access_token:
                return {"message":error_message}, 400
            
            is_valid_refresh_token, payload, error_message = self._safely_decode_refresh_token(refresh_token)
            if not is_valid_refresh_token:
                return {"message":error_message}, 400
            
            access_token = self._hash_token(access_token)
            expired_at = payload.get("exp")
            expired_at = datetime.fromtimestamp(expired_at)

            revoked_token = self.revoked_token.revoke_token(access_token, expired_at)
            if not revoked_token:
                return {"message":"Failed to revoke token"}, 500

            new_access_token = self.create_access_token(payload)
            new_refresh_token = self.create_refresh_token(payload)
            return {
                "message":"OK", 
                "data": {
                    "access_token":new_access_token,
                    "refresh_token":new_refresh_token
                }
            }, 200
        except:
            traceback.print_exc()
            return {"message":"Internal server error"}, 500
    
    
    def _decode_token(self, token: str, secret_key):
        payload = jwt.decode(
            token, 
            secret_key,
            algorithms=["HS256"],
            verify=True
        )
        return payload
    
    def _create_token(self, payload: dict, secret_key: str, expiration: int):
        payload["iat"] = datetime.utcnow()
        payload["exp"] = datetime.utcnow()+timedelta(minutes=expiration)
        token = jwt.encode(
            payload, 
            secret_key, 
            algorithm="HS256"
        )
        return token
    
    def _hash_token(self, token):
        "Hash jwt token before we store it to database."
        # encode string to bytes
        bytes_token = token.encode()
        hash = hashlib.sha256(bytes_token)

        # create hexadecimal values
        return hash.hexdigest()
    
    def _safely_decode_access_token(self, access_token):
        try:
            self.decode_access_token(access_token)
            return True, None
        except jwt.exceptions.ExpiredSignatureError:
            return True, None
        except:
            return False,"Invalid access token"
        
    def _safely_decode_refresh_token(self, refresh_token):
        try:
            payload = self.decode_refresh_token(refresh_token)
            return True, payload, None
        except jwt.exceptions.ExpiredSignatureError:
            return False, None, "Expired refresh token"
        except:
            traceback.print_exc()
            return False, None, "Invalid refresh token"
    
    