import psycopg2
from psycopg2.extras import RealDictCursor
from config.settings import get_settings
settings = get_settings()

def get_postgres_connection():
    return psycopg2.connect(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        dbname=settings.POSTGRES_DB,
        cursor_factory=RealDictCursor
    )