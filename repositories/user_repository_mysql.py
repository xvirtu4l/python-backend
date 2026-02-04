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
                "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)",
                (user.email, user.username, user.password)
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
            return [User(row["email"], row["username"], row["password"]) for row in rows]
        finally:
            cursor.close()
            session.close()
        