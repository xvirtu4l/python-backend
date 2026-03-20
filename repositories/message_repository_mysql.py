from repositories.message_repository import MessageRepository
from domain.entities.message import Message
from database.mysql_conn import get_connection
from typing import List, Optional

class MessageRepositoryMySQL(MessageRepository):
    def __init__(self, db_config):
        self.db_config = db_config
        
    def add_message(self, message: Message) -> Message:
        session = get_connection(self.db_config)
        cursor = session.cursor(dictionary=True)
        try:
            cursor.execute(
                """INSERT INTO messages (conversation_id, role, content) VALUES (%s, %s, %s)""",
                (message.conversation_id, message.role, message.content)
            )
            session.commit()
            message_id = cursor.lastrowid

            cursor.execute(
                "SELECT * FROM messages WHERE id = %s", (message_id,)
            )
            row = cursor.fetchone()
            return Message.from_db(row)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            cursor.close()
            session.close()
            
    def get_messages_by_conversation_id(self, conversation_id):
        session = get_connection(self.db_config)
        cursor = session.cursor(dictionary=True)
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