from pydantic import BaseModel


class MailBody(BaseModel):
    to: list[str]
    subject: str
    body: str
