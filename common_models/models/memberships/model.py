from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, condecimal
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID

if TYPE_CHECKING:
    from common_models.models.location.model import Location
    from common_models.models.organization.model import LinkOrgUser
    from common_models.models.price.model import Currency
    from common_models.models.user.model import User
    from common_models.models.memberships.link_membership_location import LinkMembershipLocation


class BillingType(Enum):
    one_time = "one_time"
    recurring = "recurring"


class BillingPeriod(Enum):
    day = "day"
    week = "week"
    month = "month"
    year = "year"


class MembershipType(Enum):
    unlimited = "unlimited"
    limited = "limited"
    percentage = "percentage"
    fixed = "fixed"


class Membership(SQLModel, table=True):
    __tablename__ = "memberships"
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

    expires_at: datetime = Field(nullable=True)

    name: str
    description: str
    active: bool

    currency: Currency
    amount: condecimal(max_digits=18, decimal_places=2)

    billing_type: BillingType

    billing_period: BillingPeriod
    number_of_payments: int

    membership_type: MembershipType
    value: float

    stripe_product_id: str
    stripe_price_id: str

    id_org: UUID = Field(foreign_key="org.id")

    locations: list["Location"] = Relationship(
        back_populates="memberships",
        link_model=LinkMembershipLocation,
        sa_relationship_kwargs={"lazy": "joined", "join_depth": 1},
    )

    users: list["User"] = Relationship(
        back_populates="membership",
        link_model=LinkOrgUser,
        sa_relationship_kwargs={"lazy": "joined", "join_depth": 1},
    )

    events: list["Event"] = Relationship(  # noqa: F821
        back_populates="membership",
        sa_relationship_kwargs={"lazy": "noload"},
    )

    class Write(BaseModel):
        name: str
        description: str
        active: bool

        currency: Currency
        amount: condecimal(max_digits=18, decimal_places=2)

        billing_type: BillingType

        billing_period: BillingPeriod
        number_of_payments: int

        membership_type: MembershipType
        value: condecimal(max_digits=18, decimal_places=2)

        locations: Optional[list[UUID]] = []

    class Read(BaseModel):
        id: UUID
        created_at: datetime
        expiration_date: Optional[datetime]

        name: str
        description: str
        active: bool

        currency: Currency
        amount: condecimal(max_digits=18, decimal_places=2)

        billing_type: BillingType

        billing_period: BillingPeriod
        number_of_payments: int

        membership_type: MembershipType
        value: condecimal(max_digits=18, decimal_places=2)

        stripe_product_id: str
        stripe_price_id: str

        locations: Optional[list[Location.Read]]
        users: Optional[list[User.Read]]


class SubscriptionResponse(BaseModel):
    membership: Membership.Read
    invoice_url: Optional[str]


class PaginatedMemberships(BaseModel):
    items: list[Membership.Read]

    total: int
    pages: int
