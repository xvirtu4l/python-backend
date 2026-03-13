class BusinessError(Exception):
    """Base class for business logic errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
        
class DuplicateUserError(BusinessError):
    """Raised when trying to create a user that already exists."""
    pass

class NotFoundError(BusinessError):
    """Raised when a requested resource is not found."""
    pass

class AccessDeniedError(BusinessError):
    """Raised when a user tries to access a resource they don't have permission for."""
    pass