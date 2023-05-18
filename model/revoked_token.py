from .db import Connection

class RevokedToken:

    def has_been_revoked(self, access_token: str):
        query ="""
            select 1 from revoked_token where access_token= %(access_token)s
        """
        conn = Connection()
        cursor = conn.cursor()
        cursor.execute(query, {"access_token":access_token})
        result = cursor.fetchone()
        conn.close()
        return result
    
    def revoke_token(self, access_token: str, expired_at: str):
        query ="""
            insert into revoked_token (access_token, expired_at) values (%(access_token)s, %(expired_at)s) 
        """
        conn = Connection()
        cursor = conn.cursor()
        cursor.execute(query, {"access_token":access_token, "expired_at":expired_at})
        conn.commit()
        conn.close()
        return cursor.rowcount
    
    def clear_revoked_token(self, max_expiration):
        query ="""
            delete from revoked_token where expired_at <= %(max_expiration)s
        """
        conn = Connection()
        cursor = conn.cursor()
        cursor.execute(query, {"max_expiration":max_expiration})
        conn.commit()
        conn.close()
        return cursor.rowcount
    
    
