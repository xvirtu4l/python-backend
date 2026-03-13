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
class LLMConfig:
    provider: str
    model: str
    api_key: str
    base_url: str
    http_referer: str
    x_title: str
    
@dataclass
class AppConfig:
    env: str
    db_type: str
    database: DatabaseConfig
    jwt: JWTConfig
    minio: MinIOConfig
    llm: LLMConfig

    
def get_settings() -> AppConfig:
    db_type = os.getenv("DB_TYPE", "fake")
    
    if db_type == "mysql":
        db_config = DatabaseConfig(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            name=os.getenv("DB_NAME")
        )
    elif db_type == "postgres":
        db_config = DatabaseConfig(
            host=os.getenv("POSTGRES_HOST"),
            port=int(os.getenv("POSTGRES_PORT")),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            name=os.getenv("POSTGRES_DB")
        )
        
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

    return AppConfig(
          env=os.getenv("APP_ENV", "dev"),
          db_type=os.getenv("DB_TYPE", "fake"),
          database=db_config,
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
          ),
          llm=LLMConfig(
            provider=os.getenv("LLM_PROVIDER", "openrouter"),
            model=os.getenv("LLM_MODEL", "stepfun/step-3.5-flash:free"),
            api_key=os.getenv("LLM_API_KEY"),   
            base_url=os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1"),
            http_referer=os.getenv("LLM_HTTP_REFERER", "http://localhost:8000"),
            x_title=os.getenv("LLM_X_TITLE", "Chatbot App")
        )
    )