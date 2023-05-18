from flask import Flask
from flask import request
from flask_cors import CORS

from controller.user import UserController
from controller.role_permission import RolePermissionController

app = Flask(__name__)
CORS(app)

user_controller = UserController()
role_permission_controller = RolePermissionController()

app = Flask(__name__)
CORS(app)

@app.post("/login")
def login(): 
    auth = request.authorization
    if not auth:
        return {"message":"Authentication Required"}, 400
    return user_controller.login(auth.username, auth.password)

@app.get("/permissions")
def get_permissions(): 
    role_id = request.args.get("role_id")
    return role_permission_controller.get_permissions(role_id)


if __name__== "__main__":
    app.run(port=8080, debug=True)