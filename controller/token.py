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
    
    def _create_token(self, payload: dict, secret_key: str, expiration: int):
        payload["iat"] = datetime.utcnow()
        payload["exp"] = datetime.utcnow()+timedelta(minutes=expiration)
        token = jwt.encode(
            payload, 
            secret_key, 
            algorithm="HS256"
        )
        return token