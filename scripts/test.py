import sys
from pathlib import Path

# Add parent directory to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent))
from security.password_hasher_interface import PasswordHasherImpl

hasher = PasswordHasherImpl()
hashed = hasher.hash_password("111111111")
print(hasher.verify_password("222222222", hashed))  # Phải là False
print(hasher.verify_password("111111111", hashed))  # Phải là True