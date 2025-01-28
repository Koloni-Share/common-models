from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, func
from sqlmodel import Field, SQLModel
from sqlmodel.sql.sqltypes import GUID
from common_models.util.form import as_form


class RoleType(Enum):
    admin = "admin"
    member = "member"
    viewer = "viewer"
    operator = "operator"


class PermissionType(str, Enum):
    create = "create"
    read = "read"
    update = "update"
    delete = "delete"


class Member(BaseModel):
    user_id: Optional[str]
    name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: Optional[datetime]
    email: str
    phone_number: Optional[str]
    enabled: Optional[bool] = True
    user_status: Optional[str]
    role: Optional[RoleType]
    pin_code: Optional[str]
    id_locations: Optional[list[UUID]]
    send_reported_issues: Optional[bool] = False


@as_form
class MemberUpdate(BaseModel):
    name: str
    first_name: str
    last_name: Optional[str]
    phone_number: Optional[str]
    role: Optional[RoleType]
    pin_code: Optional[str]
    id_locations: Optional[list[UUID]] = Field(default_factory=list)
    send_reported_issues: Optional[bool] = False


class MemberPatch(BaseModel):
    name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    role: Optional[RoleType]
    pin_code: Optional[str]
    id_locations: Optional[list[UUID]] = Field(default_factory=list)
    send_reported_issues: Optional[bool] = False


class PaginatedMembers(BaseModel):
    items: list[Member]

    total: int
    pages: int


class BasicResponse(BaseModel):
    detail: str


class CognitoMembersRoleLink(SQLModel, table=True):
    __tablename__ = "cognito_members_role_link"
    __table_args__ = {"extend_existing": True}

    user_id: UUID = Field(primary_key=True)  # UUID from Cognito
    role_id: UUID = Field(foreign_key="role.id", primary_key=True)


class Role(SQLModel, table=True):
    __tablename__ = "role"
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

    role: RoleType
    pin_code: Optional[str]

    user_id: str

    id_org: UUID = Field(foreign_key="org.id")
    send_reported_issues: bool = Field(
        sa_column=Column(
            Boolean,
            server_default="false",
            nullable=False,
        )
    )


class RolePermission(SQLModel, table=True):
    __tablename__ = "role_permission"
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

    role_id: UUID = Field(foreign_key="role.id", nullable=False)
    permission: PermissionType


class LinkMemberLocation(SQLModel, table=True):
    __tablename__ = "link_member_location"
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

    user_id: str = Field(nullable=False)
    id_location: UUID = Field(foreign_key="location.id")
