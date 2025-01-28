from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, SQLModel


class LinkLocationOrgShared(SQLModel, table=True):
    __tablename__ = "link_location_org_shared"

    created_at: datetime = Field(
        sa_column=Column(
            "created_at",
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

    id_org: UUID = Field(foreign_key="org.id", primary_key=True)
    id_location: UUID = Field(foreign_key="location.id", primary_key=True)
    active: bool = Field(default=False)

    class Read(BaseModel):
        id_org: UUID
        id_location: UUID
        active: bool

        class Config:
            orm_mode = True

    class Write(BaseModel):
        id_org: UUID
        id_location: UUID
        active: bool
