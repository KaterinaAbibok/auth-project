from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: int
    type: str
