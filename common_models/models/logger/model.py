from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, func
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID

from common_models.models.event.model import Event


class LogType(Enum):
    lock = "lock"
    unlock = "unlock"
    maintenance = "maintenance"
    report_issue = "report_issue"


class Log(SQLModel, table=True):
    __tablename__ = "log"
    __table_args__ = {"extend_existing": True}

    id: UUID = Field(
        sa_column=Column(
            "id",
            GUID(),
            server_default=func.gen_random_uuid(),
            unique=True,
            primary_key=True,
        )
    )
    created_at: datetime

    log_type: LogType
    log_owner: Optional[str]

    id_org: UUID = Field(foreign_key="org.id")
    id_event: Optional[UUID] = Field(
        sa_column=Column(
            "id_event",
            GUID(),
            ForeignKey("event.id", ondelete="CASCADE"),
            nullable=True,
        )
    )
    id_device: Optional[UUID] = Field(
        sa_column=Column(
            "id_device",
            GUID(),
            ForeignKey("device.id", ondelete="CASCADE"),
            nullable=True,
        )
    )

    event: Optional["Event"] = Relationship(
        back_populates="log",
        sa_relationship_kwargs={"lazy": "joined", "join_depth": 1},
    )

    class Read(BaseModel):
        id: UUID
        created_at: datetime

        log_type: LogType
        log_owner: Optional[str]

        event: Optional[Event.Read]

    class Write(BaseModel):
        log_type: LogType
        log_owner: Optional[str]
        id_event: Optional[UUID]
        id_device: Optional[UUID]
