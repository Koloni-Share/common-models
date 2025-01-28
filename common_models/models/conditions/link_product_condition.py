import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, func
from sqlmodel import Field, SQLModel
from sqlmodel.sql.sqltypes import GUID


class ConditionProductLink(SQLModel, table=True):
    __tablename__ = "condition_product_link"
    __table_args__ = {"extend_existing": True}

    condition_id: uuid.UUID = Field(
        sa_column=Column(
            "condition_id",
            GUID(),
            ForeignKey("condition.id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
        )
    )
    product_id: uuid.UUID = Field(
        sa_column=Column(
            "product_id",
            GUID(),
            ForeignKey("product.id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
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
