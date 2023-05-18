import traceback

import bcrypt

from model.user import User
from .token import TokenController

class UserController:
    def __init__(self):
        self.user = User()
        self.token = TokenController()

    def login(self, username: str, password: str):
        try:
            user = self.user.get_user(username)
            if not user:
                return {"message": "Username or Password is Incorrect"}, 400
            
            password = password.encode("utf-8")
            hashed_password = user[0].encode("utf-8")
            is_match = bcrypt.checkpw(password, hashed_password)
            if not is_match:
                return {"message": "Username or Password is Incorrect"}, 400
            
            data ={
                "user_id":user[1],
                "name":user[2],
                "role_id":user[3]
            }
            access_token = self.token.create_access_token(data)
            refresh_token = self.token.create_refresh_token(data)

            return {
                "message":"Success",
                "access_token":access_token, 
                "refresh_token":refresh_token 
            }, 200
        
        except:
            traceback.print_exc()
            return {"message": "Internal Server Error"}, 500
        

