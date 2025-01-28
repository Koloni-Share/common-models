"""
Temporal adapter for notification service
Once we have a domain for notification service, we can remove this file
"""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class NotificationSendSummaryResponse(BaseModel):
    sms: Optional[str] = Field(None, description="Details about SMS status")
    skip: Optional[str] = Field(None, description="Reason for skipping notification")
    other: Optional[str] = Field(None, description="Additional details")
    email: Optional[str] = Field(None, description="Details about email status")
    id_notification: UUID = Field(..., description="Unique notification ID")
    member: Optional[str] = Field(None, description="Details about member notification")


class CallbackRequest(BaseModel):
    version: Optional[str]
    id: Optional[str]
    detail_type: Optional[str] = Field(alias="detail-type")
    source: Optional[str]
    account: Optional[str]
    time: Optional[str]
    region: Optional[str]
    resources: Optional[list[str]]
    detail: Optional[dict]
