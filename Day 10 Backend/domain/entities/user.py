class User:
    def __init__(
        self,
        id: int | None,
        email,
        username,
        password,
        is_active: bool = True,
        created_at=None,
        updated_at=None,
        validate: bool = True
    ):
        if validate:
            self._validate_email(email)
            self._validate(email, username, password)
        self.id = id
        self.email = email
        self.username = username
        self.password = password
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
        
    @classmethod
    def from_db(cls, row: dict):
        return cls(
            id=row["id"],
            email=row["email"],
            username=row["username"],
            password=row["password"],
            is_active=row["is_active"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            validate=False
        )

    def _validate_email(self, email):
        if "@" not in email:
            raise ValueError("Invalid email address")
    
    def _validate(self, email, username, password):
        if not email:
            raise ValueError("email_required")
        
        if not username:
            raise ValueError("username_required")
        
        if not password:
            raise ValueError("password_required")

        # if len(password) < 8:
        #     raise ValueError("password_too_short")
        
        if username.lower() == "admin":
            raise ValueError("username_reserved")