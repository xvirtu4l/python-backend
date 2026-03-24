class Conversation:
    def __init__(self, id: int, user_id: int, title: str, created_at: str, updated_at: str):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.created_at = created_at
        self.updated_at = updated_at
        
        
    @classmethod
    def from_db(cls, row: dict):
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            title=row["title"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )