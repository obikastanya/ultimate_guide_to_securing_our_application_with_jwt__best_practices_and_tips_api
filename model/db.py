from psycopg2 import connect

import config

class Connection:
    def __new__(cls) -> object:
        # return the connection object.
        return connect(
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT
        )