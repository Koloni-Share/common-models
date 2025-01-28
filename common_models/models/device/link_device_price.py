from uuid import UUID

from sqlalchemy import Column, ForeignKey, func
from sqlmodel import Field, SQLModel
from sqlmodel.sql.sqltypes import GUID


class LinkDevicePrice(SQLModel, table=True):
    __tablename__ = "link_device_price"
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

    id_device: UUID = Field(
        sa_column=Column(
            "id_device", GUID(), ForeignKey("device.id", ondelete="CASCADE")
        )
    )
    id_price: UUID = Field(foreign_key="price.id")
