from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, validator
from sqlalchemy import Column, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID, AutoString
from common_models.util.form import as_form

from common_models.models.event.model import Event
from common_models.models.member.model import Member
from common_models.models.user.model import User


class IssueStatus(Enum):
    pending = "pending"
    in_progress = "in_progress"
    resolved = "resolved"


class Issue(SQLModel, table=True):
    __tablename__ = "issue"
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

    created_at: datetime = Field(
        sa_column=Column(
            "created_at",
            DateTime(timezone=True),
            server_default=func.current_timestamp(),
            nullable=False,
        )
    )

    issue_id: Optional[str]

    description: str
    pictures: Optional[list[str]] = Field(
        sa_column=Column(ARRAY(AutoString), nullable=True)
    )

    status: IssueStatus = Field(default=IssueStatus.pending)

    team_member_id: Optional[UUID] = Field(default=None, nullable=True)

    id_org: UUID = Field(foreign_key="org.id")
    id_user: Optional[UUID] = Field(foreign_key="User.id")
    id_event: Optional[UUID] = Field(
        sa_column=Column(
            "id_event",
            GUID(),
            ForeignKey("event.id", ondelete="CASCADE"),
            nullable=True,
        )
    )

    user: Optional["User"] = Relationship(
        back_populates="issues", sa_relationship_kwargs={"lazy": "joined"}
    )

    event: Optional["Event"] = Relationship(
        back_populates="issue",
        sa_relationship_kwargs={"lazy": "joined", "join_depth": 1},
    )

    class Read(BaseModel):
        id: UUID
        created_at: datetime

        issue_id: Optional[str]

        description: str
        pictures: Optional[list[str]]

        status: IssueStatus

        team_member_id: Optional[UUID]
        team_member: Optional[Member]

        id_user: Optional[UUID]
        id_event: Optional[UUID]

        user: Optional[User.Read]
        event: Optional[Event.Read]

    @as_form
    class Write(BaseModel):
        team_member_id: Optional[UUID]
        description: str
        status: IssueStatus = Field(default=IssueStatus.pending)
        id_user: Optional[UUID | str] = None  # Accept both UUID and str

        @validator('id_user', pre=True, always=True)
        def convert_null_to_none(cls, v):
            if v == "null":
                return None
            return v


class PaginatedIssues(BaseModel):
    items: list[Issue.Read]

    total: int
    pages: int
