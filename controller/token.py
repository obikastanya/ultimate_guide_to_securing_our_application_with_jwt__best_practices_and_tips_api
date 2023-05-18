from datetime import datetime, timedelta

import jwt

import config

class TokenController:

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