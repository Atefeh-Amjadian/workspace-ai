from pydantic import BaseModel


class EmailCreate(BaseModel):
    subject: str
    sender: str


class EmailResponse(BaseModel):
    id: int
    subject: str
    sender: str
    status: str

    model_config = {
        "from_attributes": True
    }