import psycopg2
from psycopg2.extras import RealDictCursor
from config.settings import get_settings

def get_postgres_connection():
    settings = get_settings()
    db_config = settings.database
    return psycopg2.connect(
        host=db_config.host,
        port=db_config.port,
        user=db_config.user,
        password=db_config.password,
        dbname=db_config.name,
        cursor_factory=RealDictCursor
    )