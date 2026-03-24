from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from usecases.chatbot_usecase import ChatbotUseCase
from factories.chatbot_factory import get_chatbot_usecase
from domain.exceptions import BusinessError, NotFoundError, AccessDeniedError, RateLimitError
from security.oauth2 import oauth2_scheme

from schemas.chatbot_schema import (
    ChatRequest,
    ChatResponse,
    MessageResponse,
    ConversationResponse,
    ConversationDetailResponse
)

router = APIRouter(prefix="/chatbot", tags=["chatbot"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: Request,
    chat_request: ChatRequest,
    chatbot_usecase: ChatbotUseCase = Depends(get_chatbot_usecase),
    token: str = Depends(oauth2_scheme)
):
    try:
        current_user = request.state.user
        user_id = current_user["id"]
        user_msg, assistant_msg = await chatbot_usecase.process_message(
            user_id=user_id,
            user_message=chat_request.message,
            conversation_id=chat_request.conversation_id
        )
        
        return ChatResponse(
            conversation_id=user_msg.conversation_id,
            user_message=MessageResponse(
                id=user_msg.id,
                role=user_msg.role,
                content=user_msg.content,
                created_at=user_msg.created_at.isoformat()
            ),
            assistant_message=MessageResponse(
                id=assistant_msg.id,
                role=assistant_msg.role,
                content=assistant_msg.content,
                created_at=assistant_msg.created_at.isoformat()
            )
        )
    except RateLimitError as e:
        raise HTTPException(status_code=429, detail=str(e))
    except BusinessError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e
        # import traceback
        # traceback.print_exc()
        # raise

@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    request: Request,
    chatbot_usecase: ChatbotUseCase = Depends(get_chatbot_usecase),
    token: str = Depends(oauth2_scheme)
):
    try:
        current_user = request.state.user
        user_id = current_user["id"]

        conversations = chatbot_usecase.list_user_conversations(user_id=user_id)
        return [
            ConversationResponse(
            id=conv.id,
            title=conv.title,
            created_at=conv.created_at.isoformat(),
            updated_at=conv.updated_at.isoformat()
        ) for conv in conversations
    ]
        
    except BusinessError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    request: Request,
    conversation_id: int,
    chatbot_usecase: ChatbotUseCase = Depends(get_chatbot_usecase),
    token: str = Depends(oauth2_scheme)
):
    try:
        current_user = request.state.user
        user_id = current_user["id"]
        
        conversation, messages = chatbot_usecase.get_conversation_history(
            user_id=user_id,
            conversation_id=conversation_id
        )
        
        return ConversationDetailResponse(
            conversation=ConversationResponse(
                id=conversation.id,
                title=conversation.title,
                created_at=conversation.created_at.isoformat(),
                updated_at=conversation.updated_at.isoformat()
            ),
            messages=[
                MessageResponse(
                    id=msg.id,
                    role=msg.role,
                    content=msg.content,
                    created_at=msg.created_at.isoformat()
                ) for msg in messages
            ]
        )
        
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Conversation not found")
    except AccessDeniedError:
        raise HTTPException(status_code=403, detail="Access denied")
    except BusinessError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    request: Request,
    conversation_id: int,
    chatbot_usecase: ChatbotUseCase = Depends(get_chatbot_usecase),
    token: str = Depends(oauth2_scheme)
):
    try:
        current_user = request.state.user
        user_id = current_user["id"]
        
        chatbot_usecase.delete_conversation(
            user_id=user_id,
            conversation_id=conversation_id
        )
        return {"message": "Conversation deleted successfully"}
    
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Conversation not found")
    except AccessDeniedError:
        raise HTTPException(status_code=403, detail="Access denied")
    except BusinessError as e:
        raise HTTPException(status_code=400, detail=str(e))
