from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class Channel(Enum):
    sms = "sms"
    email = "email"


class VerificationMessage(BaseModel):
    # The twilio verification object
    sid: str
    to: str
    channel: str
    status: str


class VerifyUserResponse(BaseModel):
    user: UUID
    is_new_user: bool
