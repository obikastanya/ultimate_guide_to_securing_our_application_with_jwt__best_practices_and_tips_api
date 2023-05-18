from flask import Flask
from flask import request
from flask_cors import CORS

from controller.user import UserController
from controller.role_permission import RolePermissionController
from controller.product import ProductController
from controller.token import TokenController

from middleware.auth import ( 
    permission_required,
    token_required
)

app = Flask(__name__)
CORS(app)

user_controller = UserController()
role_permission_controller = RolePermissionController()
product_controller = ProductController()
token_controller = TokenController()

app = Flask(__name__)
CORS(app)

@app.post("/login")
def login(): 
    auth = request.authorization
    if not auth:
        return {"message":"Authentication Required"}, 400
    return user_controller.login(auth.username, auth.password)

@app.get("/permissions")
@token_required
def get_permissions(): 
    role_id = request.user.get("role_id")
    return role_permission_controller.get_permissions(role_id)


@app.get("/products")
@token_required
@permission_required("product:view")
def get_products():
    return product_controller.get_products()


@app.post("/product")
@permission_required("product:create")
def insert_product():
    payload = request.json
    if not payload:
        return {"message":"Bad request"}, 400
    
    id = payload.get("id")
    title = payload.get("title")
    description = payload.get("description") 
    price = payload.get("price") 
    discountpercentage = payload.get("discountpercentage") 
    rating =  payload.get("rating")
    stock = payload.get("stock")
    brand = payload.get("brand")
    category = payload.get("category")

    return product_controller.insert_product(
        id = id,
        title = title,
        description = description,
        price = price,
        discountpercentage = discountpercentage,
        rating = rating,
        stock = stock,
        brand = brand,
        category = category
    )

@app.put("/product/<id>/")
@permission_required("product:update")
def update_product(id):
    payload = request.json
    if not payload:
        return {"message":"Bad request"}, 400
    
    title = payload.get("title")
    price = payload.get("price") 
    description = payload.get("description") 
    discountpercentage = payload.get("discountpercentage") 
    rating =  payload.get("rating")
    stock = payload.get("stock")
    brand = payload.get("brand")
    category = payload.get("category")

    return product_controller.update_product(
        id = id,
        title = title,
        description = description,
        price = price,
        discountpercentage = discountpercentage,
        rating = rating,
        stock = stock,
        brand = brand,
        category = category
    )

@app.get("/product/<id>/")
@permission_required("product:view")
def get_product(id):
    return product_controller.get_product(id)

@app.delete("/product/<id>/")
@permission_required("product:delete")
def delete_product(id):
    return product_controller.delete_product(id)


@app.post("/logout")
@token_required
def logout():
    access_token = request.headers.get("Authorization")
    access_token = access_token.split(" ")[1]
    return token_controller.revoke_access_token(access_token)

@app.delete("/token/revoked/clear")
@token_required
@permission_required("revoked_token:delete")
def clear_revoked_token():
    return token_controller.clear_revoked_token()

if __name__== "__main__":
    app.run(port=8080, debug=True)