from pydantic import BaseModel

class Record(BaseModel):
    name: str
    email: str
    medical_history: str