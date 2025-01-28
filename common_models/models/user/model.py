from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING
from uuid import UUID

# pylint: disable=no-name-in-module
from pydantic import BaseModel, constr
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import BOOLEAN
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID, AutoString

if TYPE_CHECKING:
    from common_models.models.login.model import Channel
    from common_models.models.organization.model import LinkOrgUser


class User(SQLModel, table=True):
    __tablename__ = "User"
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

    name: str = Field(
        sa_column=Column("name", AutoString(), server_default="User", nullable=False)
    )

    last_name: str = Field(
        sa_column=Column(
            "last_name", AutoString(), server_default="User", nullable=True
        )
    )

    active: bool = Field(
        sa_column=Column("active", BOOLEAN, server_default="true", nullable=False)
    )

    is_deleted: bool = Field(
        sa_column=Column("is_deleted", BOOLEAN, server_default="false", nullable=False)
    )

    phone_number: Optional[str] = Field(nullable=True)
    email: Optional[str] = Field(nullable=True)

    user_id: Optional[str] = Field(nullable=True)
    pin_code: Optional[str] = Field(nullable=True)
    access_code: Optional[str] = Field(nullable=True)  # read only
    address: Optional[str] = Field(nullable=True)

    require_auth: bool = Field(nullable=False, default=False)

    events: list["Event"] = Relationship(  # noqa: F821
        back_populates="user",
        sa_relationship_kwargs={
            "lazy": "noload",
            "uselist": True,
        },
    )

    issues: list["Issue"] = Relationship(  # noqa: F821
        back_populates="user",
        sa_relationship_kwargs={
            "lazy": "noload",
            "uselist": True,
        },
    )

    product_tracking: list["ProductTracking"] = Relationship(  # noqa: F821
        back_populates="user",
        sa_relationship_kwargs={
            "lazy": "noload",
            "uselist": True,
        },
    )

    reservation: Optional["Reservation"] = Relationship(  # noqa: F821
        back_populates="user",
        sa_relationship_kwargs={
            "lazy": "noload",
            "uselist": False,
        },
    )

    membership: Optional["Membership"] = Relationship(  # noqa: F821
        back_populates="users",
        link_model=LinkOrgUser,
        sa_relationship_kwargs={"lazy": "noload"},
    )

    class Write(BaseModel):
        name: str | None
        last_name: str | None
        email: str | None
        phone_number: str | None
        user_id: str | None
        pin_code: constr(regex=r"\d{4}", max_length=4) | None
        address: str | None
        active: bool = True
        require_auth: bool = False
        groups: list[str] = []

    class MobileWrite(BaseModel):
        name: Optional[str]
        last_name: Optional[str]
        address: Optional[str]
        phone_number: Optional[str]
        email: Optional[str]

    class Read(BaseModel):
        id: UUID
        created_at: datetime
        name: str
        last_name: Optional[str]
        phone_number: Optional[str]
        email: Optional[str]
        active: bool
        user_id: Optional[str]
        pin_code: Optional[str]
        access_code: Optional[str]
        address: Optional[str]
        require_auth: bool
        groups: Optional[list] = []
        is_deleted: bool


class Codes(SQLModel, table=True):
    __tablename__ = "codes"
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

    code: str = Field(sa_column=Column("code", AutoString(), nullable=False))
    id_user: UUID = Field(foreign_key="User.id")
    id_org: UUID = Field(foreign_key="org.id")


class EphemeralKeyResponse(BaseModel):
    id: str
    object: str
    associated_objects: list
    created: int
    expires: int
    livemode: bool
    secret: str


class PaymentMethodResponse(BaseModel):
    client_secret: str
    publishable_key: str
    ephemeral_key: EphemeralKeyResponse
    stripe_account_id: str
    customer_id: str


class Card(BaseModel):
    brand: str
    exp_month: int
    exp_year: int
    last4: str


class PaymentMethod(BaseModel):
    id: str
    card: Optional[Card]


class DefaultPaymentMethodResponse(BaseModel):
    default_payment_method: str
    last4: str


class PaginatedUsers(BaseModel):
    items: list[User.Read]
    total: int
    pages: int


class VerifyResponse(BaseModel):
    channel: Channel
    code_sent: int


class UserAttribute(Enum):
    PIN_CODE = "pin_code"
    EMAIL = "email"
    USERNAME = "username"
    USER_ID = "user_id"
    PHONE_NUMBER = "phone_number"
