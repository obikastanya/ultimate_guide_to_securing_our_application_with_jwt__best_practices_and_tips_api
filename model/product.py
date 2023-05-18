from .db import Connection

class Product:

    def get_product(self, id):
        query ="""
            SELECT id, title, description, price, discountpercentage, rating, 
            stock, brand, category
            FROM product where id =%(id)s
        """
        conn = Connection()
        cursor = conn.cursor()
        cursor.execute(query, {"id":id})
        result = cursor.fetchone()
        conn.close()
        return result
    
    def get_products(self):
        query ="""
            SELECT id, title, description, price, discountpercentage, rating, 
            stock, brand, category
            FROM product
        """
        conn = Connection()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result
    
    
    def insert_product(self, **parameter):
        """parameter => ( 
            id: int, title: str, price: int, discountpercentage: float, rating: float, 
            stock: int, brand: str, category: str )
        """
        query ="""
            INSERT INTO public.product(
                id, title, description, price, discountpercentage, rating, 
                stock, brand, category
            )
            VALUES (
                %(id)s, %(title)s, %(description)s, %(price)s, %(discountpercentage)s, %(rating)s, 
                %(stock)s, %(brand)s, %(category)s
            );
        """    
        conn = Connection()
        cursor = conn.cursor()
        cursor.execute(query, parameter)
        conn.commit()
        conn.close()
        return cursor.rowcount

    def update_product(self, **parameter):
        """parameter => ( 
            id, title: str, price: int, discountpercentage: float, rating: float, 
            stock: int, brand: str, category: str )
        """
        query ="""
            UPDATE public.product SET
            title = %(title)s, description = %(description)s, price =%(price)s, discountpercentage =%(discountpercentage)s, 
            rating= %(rating)s,  stock= %(stock)s, brand=%(brand)s, category=%(category)s
            WHERE id =%(id)s
        """    
        conn = Connection()
        cursor = conn.cursor()
        cursor.execute(query, parameter)
        conn.commit()
        conn.close()
        return cursor.rowcount

    def delete_product(self, id):
        query ="""
            DELETE FROM public.product WHERE id =%(id)s
        """    
        conn = Connection()
        cursor = conn.cursor()
        cursor.execute(query, {"id":id})
        conn.commit()
        conn.close()
        return cursor.rowcount


