from pydantic import BaseModel


class EmailCreate(BaseModel):
    subject: str
    sender: str
    gmail_id: str | None = None
    snippet: str | None = None
    category: str = "fyi"


class EmailResponse(BaseModel):
    id: int
    subject: str
    sender: str
    gmail_id: str | None
    snippet: str | None
    status: str
    category: str
    summary: str | None
    draft_reply: str | None

    model_config = {
        "from_attributes": True
    }