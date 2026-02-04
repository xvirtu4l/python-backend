class User:
    def __init__(self, email, username, password):
        self._validate_email(email)
        self._validate(email, username, password)
        self.email = email
        self.username = username
        self.password = password

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

        if len(password) < 8:
            raise ValueError("password_too_short")
        
        if username.lower() == "admin":
            raise ValueError("username_reserved")