import traceback

from model.product import Product

class ProductController:
    def __init__(self):
        self.product = Product()

    def insert_product(self, **parameter):
        """parameter => ( 
            id: int, title: str, price: int, discountpercentage: float, rating: float, 
            stock: int, brand: str, category: str )
        """
        try:
            record_inserted = self.product.insert_product(**parameter)
            if not record_inserted:
                return {"message":"Failed to insert"}, 500
            return {"message":"Success"}, 200
            
        except:
            traceback.print_exc()
            return {"message":"Internal Server Error"}, 500

    def update_product(self, **parameter):
        """parameter => ( 
            id: int, 
            title: str, 
            price: int, 
            discountpercentage: float, 
            rating: float, 
            stock: int, 
            brand: str, 
            category: str
        )
        """
        try:
            record_updated = self.product.update_product(**parameter)
            if not record_updated:
                return {"message":"Product is not found"}, 404
            return {"message":"Success"}, 200
        except:
            traceback.print_exc()
            return {"message":"Internal Server Error"}, 500
        
    def get_product(self, id):
        try:
            product = self.product.get_product(id)
            if not product:
                return {"message":"Product is not found", "data":{}}, 404
            data ={
                "id":product[0],
                "title":product[1], 
                "description":product[2], 
                "price":product[3], 
                "discountpercentage":product[4], 
                "rating":product[5], 
                "stock":product[6], 
                "brand":product[7], 
                "category":product[8]
            }
            return {"data":data, "message":"OK"}, 200
        except:
            traceback.print_exc()
            return {"message":"Internal server error", "data":{}}, 500
    
    def delete_product(self, id):
        try:
            record_deleted = self.product.delete_product(id)
            if not record_deleted:
                return {"message":"Product is not found"}, 404
            return {"message":"Success"}, 200
        except:
            traceback.print_exc()
            return {"message":"Internal Server Error"}, 500
    
    def get_products(self):
        try:
            products = self.product.get_products()
            if not products:
                return {"message":"No product found", "data":[]}, 404
            
            data =[]
            for product in products:
                data.append({
                    "id":product[0],
                    "title":product[1], 
                    "description":product[2], 
                    "price":product[3], 
                    "discountpercentage":product[4], 
                    "rating":product[5], 
                    "stock":product[6], 
                    "brand":product[7], 
                    "category":product[8]
                })
            return {"data":data, "message":"OK"}, 200
        except:
            traceback.print_exc()
            return {"message":"Internal server error", "data":[]}, 500
    