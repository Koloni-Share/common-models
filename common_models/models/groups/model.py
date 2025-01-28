from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, SQLModel
from sqlmodel.sql.sqltypes import GUID

if TYPE_CHECKING:
    from common_models.models.location.model import Location
    from common_models.models.user.model import User


class ResourceType(Enum):
    location = "location"
    device = "device"


class AssignmentType(Enum):
    user = "user"
    group = "group"


class Groups(SQLModel, table=True):
    __tablename__ = "groups"
    __table_args__ = {"extend_existing": True}

    id: UUID = Field(primary_key=True)

    created_at: datetime
    name: str

    id_org: UUID = Field(foreign_key="org.id")

    class Read(BaseModel):
        id: UUID
        created_at: datetime
        name: str

        users: list[User.Read]
        devices: int
        locations: list[Location.Read]


class PaginatedGroups(BaseModel):
    items: list[Groups.Read]

    total: int
    pages: int


class LinkGroupsUser(SQLModel, table=True):
    __tablename__ = "link_groups_user"
    __table_args__ = {"extend_existing": True}

    id: UUID = Field(primary_key=True)

    id_group: UUID = Field(foreign_key="groups.id")
    id_user: UUID = Field(foreign_key="User.id")


class LinkGroupsLocations(SQLModel, table=True):
    __tablename__ = "link_groups_locations"
    __table_args__ = {"extend_existing": True}

    id: UUID = Field(primary_key=True)

    id_group: UUID = Field(foreign_key="groups.id")
    id_location: UUID = Field(foreign_key="location.id")


class LinkGroupsDevices(SQLModel, table=True):
    __tablename__ = "link_groups_devices"
    __table_args__ = {"extend_existing": True}

    id: UUID = Field(primary_key=True)

    id_group: UUID = Field(foreign_key="groups.id")
    id_device: UUID = Field(
        sa_column=Column(
            "id_device",
            GUID(),
            ForeignKey("device.id", ondelete="CASCADE"),
            nullable=False,
        )
    )


class LinkUserDevices(SQLModel, table=True):
    __tablename__ = "link_user_devices"
    __table_args__ = {"extend_existing": True}

    id: UUID = Field(primary_key=True)

    id_user: UUID = Field(foreign_key="User.id")
    id_device: UUID = Field(foreign_key="device.id")


class LinkUserLocations(SQLModel, table=True):
    __tablename__ = "link_user_locations"
    __table_args__ = {"extend_existing": True}

    id: UUID = Field(primary_key=True)

    id_user: UUID = Field(foreign_key="User.id")
    id_location: UUID = Field(foreign_key="location.id")
