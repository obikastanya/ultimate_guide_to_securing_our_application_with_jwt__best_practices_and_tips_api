from .db import Connection

class User:

    def get_user(self, username):
        query ="""
            select password, id, name, role_id from public.user where username =%(username)s
        """
        conn = Connection()
        cursor = conn.cursor()
        cursor.execute(query, {"username":username})
        result = cursor.fetchone()
        conn.close()
        return result
    
