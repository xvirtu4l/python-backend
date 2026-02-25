class BusinessError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
        
class DuplicateUserError(BusinessError):
    pass