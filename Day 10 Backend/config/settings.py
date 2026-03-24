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
class EmailConfig:
    enabled: bool
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    from_email: str
    from_name: str
    use_tls: bool
    use_ssl: bool

@dataclass
class ChatConfig:
    max_user_message_length: int
    max_conversations_per_user: int
    max_messages_per_conversation: int
    max_history_messages_for_model: int
    rate_limit_window_seconds: int
    rate_limit_requests_per_window: int
    
@dataclass
class AppConfig:
    env: str
    db_type: str
    database: DatabaseConfig
    jwt: JWTConfig
    minio: MinIOConfig
    llm: LLMConfig
    email: EmailConfig
    chat: ChatConfig
    frontend_url: str


def _get_bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}

    
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
        ),
          email=EmailConfig(
            enabled=_get_bool_env("EMAIL_ENABLED", False),
            smtp_host=os.getenv("SMTP_HOST", ""),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            smtp_username=os.getenv("SMTP_USERNAME", ""),
            smtp_password=os.getenv("SMTP_PASSWORD", ""),
            from_email=os.getenv("SMTP_FROM_EMAIL", ""),
            from_name=os.getenv("SMTP_FROM_NAME", "Chatbox"),
            use_tls=_get_bool_env("SMTP_USE_TLS", True),
            use_ssl=_get_bool_env("SMTP_USE_SSL", False)
        ),
          chat=ChatConfig(
            max_user_message_length=int(os.getenv("CHAT_MAX_USER_MESSAGE_LENGTH", "2000")),
            max_conversations_per_user=int(os.getenv("CHAT_MAX_CONVERSATIONS_PER_USER", "50")),
            max_messages_per_conversation=int(os.getenv("CHAT_MAX_MESSAGES_PER_CONVERSATION", "100")),
            max_history_messages_for_model=int(os.getenv("CHAT_MAX_HISTORY_MESSAGES_FOR_MODEL", "20")),
            rate_limit_window_seconds=int(os.getenv("CHAT_RATE_LIMIT_WINDOW_SECONDS", "60")),
            rate_limit_requests_per_window=int(os.getenv("CHAT_RATE_LIMIT_REQUESTS_PER_WINDOW", "10"))
        ),
          frontend_url=os.getenv("FRONTEND_URL", "http://localhost:3000")
    )
