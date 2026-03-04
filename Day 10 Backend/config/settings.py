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
class JWTConfig:
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
        
@dataclass
class MinIOConfig:
    endpoint: str
    access_key: str
    secret_key: str
    bucket: str
    
    
    
@dataclass
class AppConfig:
    env: str
    db_type: str
    database: DatabaseConfig
    jwt: JWTConfig
    minio: MinIOConfig


    
def get_settings() -> AppConfig:
    return AppConfig(
          env=os.getenv("APP_ENV", "dev"),
          db_type=os.getenv("DB_TYPE", "fake"),
          database=DatabaseConfig(
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT")),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                name=os.getenv("DB_NAME"),
          ),
          jwt=JWTConfig(
              secret_key=os.getenv("SECRET_KEY"),
              algorithm=os.getenv("ALGORITHM", "HS256"),
              access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
          ),
          minio=MinIOConfig(
              endpoint=os.getenv("MINIO_ENDPOINT", "localhost:9000"),
                access_key=os.getenv("MINIO_ACCESS_KEY"),
                secret_key=os.getenv("MINIO_SECRET_KEY"),
                bucket=os.getenv("MINIO_BUCKET", "avatars")
          )
    )