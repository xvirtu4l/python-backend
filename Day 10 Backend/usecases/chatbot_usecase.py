from typing import List, Optional
from domain.entities.conversation import Conversation
from domain.entities.message import Message
from repositories.conversation_repository import ConversationRepository
from repositories.message_repository import MessageRepository
from repositories.llm_repository import LLMRepository
from repositories.user_repository import UserRepository
from domain.exceptions import BusinessError

class ChatbotUseCase:
    def __init__(
        self,
        message_repo: MessageRepository,
        conversation_repo: ConversationRepository,
        llm_repo: LLMRepository,
        user_repo: UserRepository
    ):
        self.message_repo = message_repo
        self.conversation_repo = conversation_repo
        self.llm_repo = llm_repo
        self.user_repo = user_repo
        
        
    async def process_message(
        self, user_id: int, user_message: str, conversation_id: Optional[int] = None
    ):
        
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise BusinessError("User not found")
        if not user.is_active:
            raise BusinessError("Account disabled.")
        
        if conversation_id:
            conversation = self.conversation_repo.get_conversation_by_id(conversation_id)
            if not conversation:
                raise BusinessError("Conversation not found")
            if conversation.user_id != user_id:
                raise BusinessError("Access denied to this conversation")
        
        if conversation_id is None:
            conversation = self.conversation_repo.create_conversation(user_id, title=user_message[:50] if len(user_message) > 50 else user_message)
            conversation_id = conversation.id
            message_history = []
            
        else:
            previous_message = self.message_repo.get_messages_by_conversation_id(conversation_id)
            message_history = [
                {"role": msg.role, "content": msg.content} for msg in previous_message
            ]
            
        user_msg = self.message_repo.add_message(
            Message(
                id=None,
                conversation_id=conversation_id,
                role="user",
                content=user_message,
                created_at=str | None
            )
        )
        
        all_messages = message_history + [{"role": "user", "content": user_message}]
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
            raise BusinessError("Conversation not found")
        if conversation.user_id != user_id:
            raise BusinessError("Access denied.")
        
        messages = self.message_repo.get_messages_by_conversation_id(conversation_id)
        return conversation, messages
    
    def list_user_conversations(self, user_id: int) -> List[Conversation]:
        conversations = self.conversation_repo.get_conversations_by_user_id(user_id)
        return conversations
    
    def delete_conversation(self, user_id: int, conversation_id: int):
        conversation = self.conversation_repo.get_conversation_by_id(conversation_id)
        if not conversation:
            raise BusinessError("Conversation not found")
        if conversation.user_id != user_id:
            raise BusinessError("Access denied.")
        
        # Note: Should check if the table has cascading delete for messages, otherwise need to delete messages first
        self.conversation_repo.delete_conversation(conversation_id)