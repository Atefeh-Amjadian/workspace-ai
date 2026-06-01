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
    summary: str | None
    draft_reply: str | None

    model_config = {
        "from_attributes": True
    }