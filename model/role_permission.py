from .db import Connection

class RolePermission:
    
    def get_permissions(self, role_id):
        query ="""
            select permission_id from role_permission where role_id= %(role_id)s
        """
        conn = Connection()
        cursor = conn.cursor()
        cursor.execute(query, {"role_id":role_id})
        result = cursor.fetchall()
        conn.close()
        return result
    
    def has_permission(self, role_id, required_permisssion):
        query ="""
            select 1 from role_permission where role_id= %(role_id)s and permission_id=%(permission_id)s
        """
        conn = Connection()
        cursor = conn.cursor()
        cursor.execute(query, {"role_id":role_id, "permission_id":required_permisssion})
        result = cursor.fetchone()
        conn.close()
        return result