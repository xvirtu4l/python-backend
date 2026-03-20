#   Script này dùng để hash lại tất cả mật khẩu người dùng đã đăng ký trước trong cơ sở dữ liệu.

import sys
from pathlib import Path

# Add parent directory to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

import mysql.connector
from usecases.password_hasher import hash_password

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "projectb"
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

cursor.execute("SELECT id, password FROM users")
users = cursor.fetchall()

for user_id, plain_password in users:
    hashed = hash_password(plain_password)
    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed, user_id))
    print(f"Hashed password for user {user_id}")

conn.commit()
cursor.close()
conn.close()
print("All passwords hashed!")