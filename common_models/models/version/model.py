from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, func
from sqlmodel import Field, SQLModel
from sqlmodel.sql.sqltypes import GUID


class MobileOperatingSystem(str, Enum):
    Android = "ANDROID"
    IOS = "IOS"


class MobileVersionRequest(BaseModel):
    app_name: str
    uri_link: Optional[str]
    app_version: str = Field(..., regex=r'^\d+(\.\d+)*$')
    app_operation_system: MobileOperatingSystem
    id_location: UUID = Field(..., description="Location Id")


class MobileVersion(SQLModel, table=True):
    __tablename__ = "mobile_version"

    id: UUID = Field(
        sa_column=Column(
            "id",
            GUID(),
            server_default=func.gen_random_uuid(),
            primary_key=True,
            nullable=False,
        )
    )

    created_at: datetime = Field(
        sa_column=Column(
            "created_at",
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

    app_name: str = Field(sa_column=Column("app_name", String, nullable=False))

    app_version: str = Field(sa_column=Column("app_version", String, nullable=False))

    previous_version: str = Field(
        sa_column=Column("previous_version", String, nullable=True)
    )

    active: bool = Field(
        sa_column=Column("active", Boolean, server_default=func.false(), nullable=False)
    )

    updated_at: datetime = Field(
        sa_column=Column(
            "updated_at",
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

    app_operation_system: MobileOperatingSystem = Field(
        sa_column=Column("app_operation_system", String, nullable=False)
    )

    id_location: UUID = Field(
        sa_column=Column(
            "id_location",
            GUID(),
            ForeignKey("location.id", ondelete="CASCADE"),
            nullable=False,
        ),
        description="Location Id",
    )
    uri_link: Optional[str] = Field(sa_column=Column("uri_link", String, nullable=True))

    class Read(BaseModel):
        id: UUID
        created_at: datetime
        updated_at: datetime
        app_name: str
        app_version: str
        previous_version: Optional[str]
        app_operation_system: str
        id_location: UUID
        uri_link: Optional[str]

        class Config:
            orm_mode = True
