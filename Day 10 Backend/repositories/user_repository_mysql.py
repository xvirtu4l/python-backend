from repositories.user_repository import UserRepository
from domain.entities.user import User
from database.mysql_conn import get_connection
from mysql.connector.errors import IntegrityError
from domain.exceptions import DuplicateUserError

class UserRepositoryMySQL(UserRepository):
    def __init__(self, db_config):
        self.db_config = db_config

    def add_user(self, user: User):
        session = get_connection(self.db_config)
        cursor = session.cursor()
        try:
            cursor.execute(
                """INSERT INTO users (email, username, password, is_active) VALUES (%s, %s, %s, %s)""",
                (user.email, user.username, user.password, user.is_active)
            )
            session.commit()
        except IntegrityError:
            session.rollback()
            raise DuplicateUserError("Email hoặc tên người dùng đã tồn tại")
        finally:
            cursor.close()
            session.close()
            
    def get_all_users(self):
        session = get_connection(self.db_config)
        cursor = session.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            return [User.from_db(row) for row in rows]
        finally:
            cursor.close()
            session.close()
            
            
    def get_user_by_username(self, username):
        session = get_connection(self.db_config)
        cursor = session.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, email, username, password, is_active, created_at, updated_at FROM users WHERE username = %s", (username,))
            row = cursor.fetchone()
            if row:
                return User.from_db(row)
        finally:
            cursor.close()
            session.close()
            