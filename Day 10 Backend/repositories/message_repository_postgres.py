from repositories.message_repository import MessageRepository
from domain.entities.message import Message
from database.postgres_conn import get_postgres_connection
from typing import List, Optional

class MessageRepositoryPostgres(MessageRepository):
    def __init__(self):
        pass
        
    def add_message(self, message: Message) -> Message:
        session = get_postgres_connection()
        cursor = session.cursor()
        try:
            cursor.execute(
                """INSERT INTO messages (conversation_id, role, content) VALUES (%s, %s, %s) RETURNING *""",
                (message.conversation_id, message.role, message.content)
            )
            row = cursor.fetchone()
            session.commit()
            return Message.from_db(row)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            cursor.close()
            session.close()
            
    def get_messages_by_conversation_id(self, conversation_id):
        session = get_postgres_connection()
        cursor = session.cursor()
        try:
            cursor.execute(
                "SELECT * FROM messages WHERE conversation_id = %s ORDER BY created_at ASC",
                (conversation_id,)
            )
            rows = cursor.fetchall()
            return [Message.from_db(row) for row in rows]
        except Exception as e:
            session.rollback()
            raise e
        finally:
            cursor.close()
            session.close()