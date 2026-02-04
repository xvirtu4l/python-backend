import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass
class DatabaseConfig:
    host: str
    port: int
    name: str
    user: str
    password: str
    
@dataclass
class AppConfig:
    env: str
    db_type: str
    database: DatabaseConfig
    
def get_settings() -> AppConfig:
    return AppConfig(
          env=os.getenv("APP_ENV", "dev"),
          db_type=os.getenv("DB_TYPE", "fake"),
          database=DatabaseConfig(
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT", 3306)),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                name=os.getenv("DB_NAME"),
          )
    )