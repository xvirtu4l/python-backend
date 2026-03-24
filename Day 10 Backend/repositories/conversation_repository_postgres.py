from repositories.conversation_repository import ConversationRepository
from domain.entities.conversation import Conversation
from database.postgres_conn import get_postgres_connection
from typing import List, Optional

class ConversationRepositoryPostgres(ConversationRepository):
    def __init__(self):
        pass
        
    def create_conversation(self, user_id, title):
        session = get_postgres_connection()
        cursor = session.cursor()
        try:
            cursor.execute(
                "INSERT INTO conversations (user_id, title) VALUES (%s, %s) RETURNING *",
                (user_id, title)
            )
            
            row = cursor.fetchone()
            session.commit()
            
            # conversation_id = cursor.lastrowid
            
            # Fetch the full row with timestamps
            # cursor.execute(
            #     "SELECT * FROM conversations WHERE id = %s",
            #     (conversation_id,)
            # )
            # row = cursor.fetchone()
            
            
            return Conversation.from_db(row)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            cursor.close()
            session.close()
            
    def get_conversations_by_user_id(self, user_id) -> List[Conversation]:
        session = get_postgres_connection()
        cursor = session.cursor()
        try:
            cursor.execute(
                "SELECT * FROM conversations WHERE user_id = %s",
                (user_id,)
            )
            rows = cursor.fetchall()
            return [Conversation.from_db(row) for row in rows]
        finally:
            cursor.close()
            session.close()
            
    def get_conversation_by_user_id(self, user_id) -> Optional[Conversation]:
        session = get_postgres_connection()
        cursor = session.cursor()
        try:
            cursor.execute(
                "SELECT * FROM conversations WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
                (user_id,)
            )
            row = cursor.fetchone()
            if row:
                return Conversation.from_db(row)
            return None
        finally:
            cursor.close()
            session.close()
            
    def get_conversation_by_id(self, conversation_id) -> Optional[Conversation]:
        session = get_postgres_connection()
        cursor = session.cursor()
        try:
            cursor.execute(
                "SELECT * FROM conversations WHERE id = %s",
                (conversation_id,)
            )
            row = cursor.fetchone()
            if row:
                return Conversation.from_db(row)
            return None
        finally:
            cursor.close()
            session.close()
            
    def delete_conversation(self, conversation_id):
        session = get_postgres_connection()
        cursor = session.cursor()
        try:
            cursor.execute(
                "DELETE FROM conversations WHERE id = %s",
                (conversation_id,)
            )
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            cursor.close()
            session.close()
