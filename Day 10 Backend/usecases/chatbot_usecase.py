from collections import defaultdict, deque
from time import time
from typing import List, Optional

from config.settings import ChatConfig
from domain.entities.conversation import Conversation
from domain.entities.message import Message
from repositories.conversation_repository import ConversationRepository
from repositories.message_repository import MessageRepository
from repositories.llm_repository import LLMRepository
from repositories.user_repository import UserRepository
from domain.exceptions import BusinessError, AccessDeniedError, NotFoundError, RateLimitError

USER_REQUEST_LOG: dict[int, deque[float]] = defaultdict(deque)

class ChatbotUseCase:
    def __init__(
        self,
        message_repo: MessageRepository,
        conversation_repo: ConversationRepository,
        llm_repo: LLMRepository,
        user_repo: UserRepository,
        chat_config: ChatConfig,
    ):
        self.message_repo = message_repo
        self.conversation_repo = conversation_repo
        self.llm_repo = llm_repo
        self.user_repo = user_repo
        self.chat_config = chat_config
        
        
    async def process_message(
        self, user_id: int, user_message: str, conversation_id: Optional[int] = None
    ):
        normalized_message, conversation_id, message_history = self._prepare_message_context(
            user_id=user_id,
            user_message=user_message,
            conversation_id=conversation_id,
        )
            
        user_msg = self.message_repo.add_message(
            Message(
                id=None,
                conversation_id=conversation_id,
                role="user",
                content=normalized_message,
                created_at=str | None
            )
        )
        
        all_messages = message_history + [{"role": "user", "content": normalized_message}]
        try:
            assistant_response = await self.llm_repo.generate_response(all_messages)
        except Exception as e:
            raise BusinessError("Failed to generate response from AI assistant") from e
        
        assistant_msg = self.message_repo.add_message(
            Message(
                id=None,
                conversation_id=conversation_id,
                role="assistant",
                content=assistant_response,
                created_at=str | None
            )
        )
        return user_msg, assistant_msg

    def get_conversation_history(self, user_id: int, conversation_id: int) -> List[Message]:
        conversation = self.conversation_repo.get_conversation_by_id(conversation_id)
        if not conversation:
            raise NotFoundError("Conversation not found")
        if conversation.user_id != user_id:
            raise AccessDeniedError("Access denied.")
        
        messages = self.message_repo.get_messages_by_conversation_id(conversation_id)
        return conversation, messages
    
    def list_user_conversations(self, user_id: int) -> List[Conversation]:
        conversations = self.conversation_repo.get_conversations_by_user_id(user_id)
        return conversations
    
    def delete_conversation(self, user_id: int, conversation_id: int):
        conversation = self.conversation_repo.get_conversation_by_id(conversation_id)
        if not conversation:
            raise NotFoundError("Conversation not found")
        if conversation.user_id != user_id:
            raise AccessDeniedError("Access denied.")
        
        # Note: Should check if the table has cascading delete for messages, otherwise need to delete messages first
        self.conversation_repo.delete_conversation(conversation_id)

    def _prepare_message_context(
        self, user_id: int, user_message: str, conversation_id: Optional[int] = None
    ):
        normalized_message = user_message.strip()

        if not normalized_message:
            raise BusinessError("Message cannot be empty")
        if len(normalized_message) > self.chat_config.max_user_message_length:
            raise BusinessError(
                f"Message too long. Maximum length is {self.chat_config.max_user_message_length} characters"
            )

        self._enforce_rate_limit(user_id)

        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        if not user.is_active:
            raise BusinessError("Account disabled.")
        
        if conversation_id:
            conversation = self.conversation_repo.get_conversation_by_id(conversation_id)
            if not conversation:
                raise NotFoundError("Conversation not found")
            if conversation.user_id != user_id:
                raise AccessDeniedError("Access denied to this conversation")
        
        if conversation_id is None:
            user_conversations = self.conversation_repo.get_conversations_by_user_id(user_id)
            if len(user_conversations) >= self.chat_config.max_conversations_per_user:
                raise BusinessError(
                    f"Conversation limit reached. Maximum is {self.chat_config.max_conversations_per_user} conversations per user"
                )

            conversation = self.conversation_repo.create_conversation(
                user_id,
                title=normalized_message[:50] if len(normalized_message) > 50 else normalized_message
            )
            conversation_id = conversation.id
            message_history = []
        else:
            previous_message = self.message_repo.get_messages_by_conversation_id(conversation_id)
            if len(previous_message) >= self.chat_config.max_messages_per_conversation:
                raise BusinessError(
                    f"Conversation limit reached. Maximum is {self.chat_config.max_messages_per_conversation} messages per conversation"
                )
            message_history = [
                {"role": msg.role, "content": msg.content}
                for msg in previous_message[-self.chat_config.max_history_messages_for_model:]
            ]

        return normalized_message, conversation_id, message_history

    def _enforce_rate_limit(self, user_id: int):
        now = time()
        user_requests = USER_REQUEST_LOG[user_id]

        while (
            user_requests
            and now - user_requests[0] > self.chat_config.rate_limit_window_seconds
        ):
            user_requests.popleft()

        if len(user_requests) >= self.chat_config.rate_limit_requests_per_window:
            raise RateLimitError(
                "Too many messages sent. "
                f"Limit is {self.chat_config.rate_limit_requests_per_window} requests "
                f"per {self.chat_config.rate_limit_window_seconds} seconds"
            )

        user_requests.append(now)
