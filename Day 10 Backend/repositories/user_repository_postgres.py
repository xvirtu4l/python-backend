from repositories.user_repository import UserRepository
from domain.entities.user import User
from database.postgres_conn import get_postgres_connection
from psycopg2.errors import UniqueViolation
from domain.exceptions import DuplicateUserError


class UserRepositoryPostgres(UserRepository):
    def __init__(self):
        pass

    def add_user(self, user: User):
        session = get_postgres_connection()
        cursor = session.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO users (email, username, password, is_active)
                VALUES (%s, %s, %s, %s)
                """,
                (user.email, user.username, user.password, user.is_active),
            )
            session.commit()
        except UniqueViolation:
            session.rollback()
            raise DuplicateUserError("Email hoặc tên người dùng đã tồn tại")
        finally:
            cursor.close()
            session.close()

    def get_all_users(self):
        session = get_postgres_connection()
        cursor = session.cursor()
        try:
            cursor.execute("SELECT email, username, password FROM users")
            rows = cursor.fetchall()
            return [User.from_db(row) for row in rows]
        finally:
            cursor.close()
            session.close()

    def get_user_by_username(self, username):
        session = get_postgres_connection()
        cursor = session.cursor()
        try:
            cursor.execute(
                "SELECT email, username, password FROM users WHERE username = %s",
                (username,),
            )
            row = cursor.fetchone()
            if row:
                return User.from_db(row)
            return None
        finally:
            cursor.close()
            session.close()
            
    