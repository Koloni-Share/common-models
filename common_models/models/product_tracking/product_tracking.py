from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, func
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID

from common_models.models.conditions.model import Condition

from common_models.models.user.model import User


class State(Enum):
    new = "new"
    incoming = "incoming"
    outgoing = "outgoing"
    maintenance = "maintenance"


class ProductTracking(SQLModel, table=True):
    __tablename__ = "product_tracking"
    __table_args__ = {"extend_existing": True}

    id: UUID = Field(
        sa_column=Column(
            "id",
            GUID,
            server_default=func.gen_random_uuid(),
            primary_key=True,
            unique=True,
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

    state: State = Field(default=State.new)

    id_org: UUID = Field(foreign_key="org.id")
    id_product: UUID = Field(foreign_key="product.id")
    id_user: Optional[UUID] = Field(foreign_key="User.id")
    id_device: Optional[UUID] = Field(
        sa_column=Column(
            "id_device",
            GUID(),
            ForeignKey("device.id", ondelete="CASCADE"),
            nullable=True,
        )
    )
    id_condition: Optional[UUID] = Field(foreign_key="condition.id")

    product: Optional["Product"] = Relationship(  # noqa: F821
        back_populates="product_tracking",
        sa_relationship_kwargs={"lazy": "noload"},
    )

    user: Optional["User"] = Relationship(
        back_populates="product_tracking",
        sa_relationship_kwargs={"lazy": "joined", "join_depth": 2},
    )

    device: Optional["Device"] = Relationship(  # noqa: F821
        back_populates="product_tracking",
        sa_relationship_kwargs={"lazy": "joined", "join_depth": 2},
    )

    condition: Optional["Condition"] = Relationship(  # noqa: F821
        back_populates="product_tracking",
        sa_relationship_kwargs={"lazy": "joined", "join_depth": 2},
    )

    class Read(BaseModel):
        created_at: datetime
        state: State
        id_product: UUID
        id_user: Optional[UUID]
        id_device: Optional[UUID]
        id_condition: Optional[UUID]

        user: Optional[User.Read]
        device: Optional[object]
        condition: Optional[Condition.Read]
