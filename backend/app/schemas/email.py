from pydantic import BaseModel


class EmailCreate(BaseModel):
    subject: str
    sender: str
    category: str = "fyi"


class EmailResponse(BaseModel):
    id: int
    subject: str
    sender: str
    status: str
    category: str

    model_config = {
        "from_attributes": True
    }