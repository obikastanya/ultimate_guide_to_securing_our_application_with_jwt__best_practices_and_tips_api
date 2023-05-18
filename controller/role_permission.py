import traceback

from model.role_permission import RolePermission

class RolePermissionController:
    def __init__(self):
        self.role_permission = RolePermission()
        
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