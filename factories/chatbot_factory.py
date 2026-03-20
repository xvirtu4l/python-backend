from config.settings import get_settings
from repositories.llm_repository_openrouter import OpenRouterLLMRepository

from repositories.conversation_repository_mysql import ConversationRepositoryMySQL
from repositories.message_repository_mysql import MessageRepositoryMySQL

from repositories.conversation_repository_postgres import ConversationRepositoryPostgres
from repositories.message_repository_postgres import MessageRepositoryPostgres

from repositories.conversation_repository import ConversationRepository
from repositories.message_repository import MessageRepository
from repositories.llm_repository import LLMRepository
from repositories.user_repository import UserRepository

from usecases.chatbot_usecase import ChatbotUseCase

from factories.user_factory import get_user_usecase

def get_llm_repository() -> LLMRepository:
    settings = get_settings()
    provider = settings.llm.provider
    
    if provider == "openrouter":
        return OpenRouterLLMRepository(config=settings.llm)
    
    elif provider == "openai":
        raise ValueError(f"LLM provider '{provider}' is not implemented yet")
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
    
def get_conversation_repository() -> ConversationRepository:
    settings = get_settings()
    db_type = settings.db_type

    if db_type == "mysql":
        return ConversationRepositoryMySQL(db_config=settings.database)
    elif db_type == "postgres":

        return ConversationRepositoryPostgres()
    elif db_type == "fake":
        # Return a fake in-memory conversation repository for testing
        pass
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
    
    
def get_message_repository() -> MessageRepository:
    settings = get_settings()
    db_type = settings.db_type
    
    if db_type == "mysql":
        return MessageRepositoryMySQL(db_config=settings.database)
    elif db_type == "postgres":
        return MessageRepositoryPostgres()
    elif db_type == "fake":
        # Return a fake in-memory message repository for testing
        pass
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
    
    


def get_chatbot_usecase() -> ChatbotUseCase:
    message_repo = get_message_repository()
    conversation_repo = get_conversation_repository()
    llm_repo = get_llm_repository()
    user_repo = get_user_usecase().repo
    
    return ChatbotUseCase(
        message_repo=message_repo,
        conversation_repo=conversation_repo,
        llm_repo=llm_repo,
        user_repo=user_repo
    )