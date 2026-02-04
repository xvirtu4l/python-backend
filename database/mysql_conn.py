import mysql.connector
from config.settings import DatabaseConfig

def get_connection(db_config: DatabaseConfig):
    return mysql.connector.connect(
        host=db_config.host,
        port=db_config.port,
        user=db_config.user,
        password=db_config.password,
        database=db_config.name
    )
