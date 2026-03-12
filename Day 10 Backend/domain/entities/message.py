class Message:
    def __init__(self, id: int, conversation_id: int, role: str, content: str, created_at: str):
        self.id = id
        self.conversation_id = conversation_id
        self.role = role
        self.content = content
        self.created_at = created_at
        
    @classmethod
    def from_db(cls, row: dict):
        return cls(
            id=row["id"],
            conversation_id=row["conversation_id"],
            role=row["role"],
            content=row["content"],
            created_at=row["created_at"]
        )