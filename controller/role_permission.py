import traceback

from model.role_permission import RolePermission

class RolePermissionController:
    def __init__(self):
        self.role_permission = RolePermission()
    
    def has_permission(self, role_id: str, required_permission: str) -> bool:
        try:
            is_has_permission = self.role_permission.has_permission(
                role_id,
                required_permission
            )
            return bool(is_has_permission)
        except:
            traceback.print_exc()
            return False
        
    def get_permissions(self, role_id: str) -> dict:
        try:
            permissions = self.role_permission.get_permissions(role_id)
            if permissions:
                permissions = [ row[0] for row in permissions ]
            else:
                permissions = []

            return { "data":{ 
                        "role_id":role_id,
                        "permissions":permissions
                    }, 
                    "message":"OK"
                }, 200
        except:
            traceback.print_exc()
            return { "data":{
                        "role_id":role_id,
                        "permissions":[]
                    }, 
                    "message":"Internal server eroor"
                }, 500