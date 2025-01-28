from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID

from common_models.models.device.model import Device, Mode
from pydantic import BaseModel, conint, constr
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, func
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID

from common_models.models.location.model import Location
from common_models.models.products.model import Product
from common_models.models.settings.model import ResTimeUnit
from common_models.models.size.model import Size
from common_models.models.user.model import User


class Reservation(SQLModel, table=True):
    __tablename__ = "reservation"
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

    tracking_number: str = ""
    mode: Mode

    recurring: Optional[bool] = Field(default=False)

    sunday: Optional[bool] = Field(default=False)
    monday: Optional[bool] = Field(default=False)
    tuesday: Optional[bool] = Field(default=False)
    wednesday: Optional[bool] = Field(default=False)
    thursday: Optional[bool] = Field(default=False)
    friday: Optional[bool] = Field(default=False)
    saturday: Optional[bool] = Field(default=False)

    # 24 hour time, example: 13:00
    from_time: Optional[constr(regex=r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")] = Field(
        nullable=False
    )
    to_time: Optional[constr(regex=r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")] = Field(
        nullable=False
    )

    start_date: Optional[datetime] = Field(
        sa_column=Column("start_date", DateTime(timezone=True))
    )
    end_date: Optional[datetime] = Field(
        sa_column=Column("end_date", DateTime(timezone=True))
    )

    id_org: UUID = Field(foreign_key="org.id")
    id_user: Optional[UUID] = Field(foreign_key="User.id")
    id_device: UUID = Field(
        sa_column=Column(
            "id_device", GUID(), ForeignKey("device.id", ondelete="CASCADE")
        )
    )
    id_location: Optional[UUID] = Field(foreign_key="location.id")
    id_size: Optional[UUID] = Field(foreign_key="size.id")
    id_product: Optional[UUID] = Field(foreign_key="product.id")

    started: bool = Field(
        sa_column=Column("started", Boolean, default=False, nullable=False)
    )

    user: Optional["User"] = Relationship(
        back_populates="reservation",
        sa_relationship_kwargs={"lazy": "joined", "uselist": False, "join_depth": 1},
    )

    device: Optional["Device"] = Relationship(
        back_populates="reservation",
        sa_relationship_kwargs={"lazy": "joined", "uselist": False, "join_depth": 1},
    )

    location: Optional["Location"] = Relationship(
        back_populates="reservation",
        sa_relationship_kwargs={"lazy": "joined", "uselist": False, "join_depth": 1},
    )

    size: Optional["Size"] = Relationship(
        back_populates="reservation",
        sa_relationship_kwargs={"lazy": "joined", "uselist": False, "join_depth": 1},
    )

    product: Optional["Product"] = Relationship(
        back_populates="reservation",
        sa_relationship_kwargs={"lazy": "joined", "uselist": False, "join_depth": 1},
    )

    sender_details: Optional[str] = Field(
        sa_column=Column(
            "sender_details",
            String(250),
            nullable=True,
        )
    )

    class Write(BaseModel):
        tracking_number: str = ""
        mode: Optional[Mode] = Mode.delivery
        recurring: Optional[bool]

        monday: Optional[bool]
        tuesday: Optional[bool]
        wednesday: Optional[bool]
        thursday: Optional[bool]
        friday: Optional[bool]
        saturday: Optional[bool]
        sunday: Optional[bool]

        from_time: Optional[constr(regex=r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")]
        to_time: Optional[constr(regex=r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")]

        start_date: Optional[datetime]
        end_date: Optional[datetime]

        user_name: Optional[str]
        phone_number: Optional[str]
        email: Optional[str]

        id_user: Optional[UUID]
        id_device: Optional[UUID]
        id_location: Optional[UUID]
        id_size: Optional[UUID]
        id_product: Optional[UUID]
        sender_details: Optional[str]
        size_external_id: Optional[str]
        user_external_id: Optional[str]

    class WriteCSV(BaseModel):
        mode: Optional[Mode] = Mode.delivery
        tracking_number: str = ""

        user_name: Optional[str]
        phone_number: Optional[str]
        email: Optional[str]

        location: Optional[str]
        size: Optional[str]

        from_time: Optional[constr(regex=r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")]
        to_time: Optional[constr(regex=r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")]

    class Batch(BaseModel):
        recurring: bool

        monday: bool
        tuesday: bool
        wednesday: bool
        thursday: bool
        friday: bool
        saturday: bool
        sunday: bool

        from_time: Optional[
            constr(regex=r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")
        ] = "00:00"
        to_time: Optional[
            constr(regex=r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")
        ] = "23:59"

        start_date: Optional[datetime] = datetime.utcnow()
        end_date: Optional[datetime]

        id_user: Optional[UUID]
        id_device: Optional[UUID]
        id_location: Optional[UUID]
        id_sizes: list[UUID] = []
        id_product: Optional[UUID]
        sender_details: Optional[str]

    class Read(BaseModel):
        id: UUID
        created_at: datetime

        mode: Mode

        tracking_number: str | None = ""
        recurring: Optional[bool]

        sunday: Optional[bool]
        monday: Optional[bool]
        tuesday: Optional[bool]
        wednesday: Optional[bool]
        thursday: Optional[bool]
        friday: Optional[bool]
        saturday: Optional[bool]

        from_time: Optional[constr(regex=r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")]
        to_time: Optional[constr(regex=r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")]

        start_date: Optional[datetime]
        end_date: Optional[datetime]

        id_user: Optional[UUID]
        id_device: Optional[UUID]
        id_location: Optional[UUID]
        id_size: Optional[UUID]
        id_product: Optional[UUID]

        started: bool

        user: Optional[User.Read]
        device: Optional[Device.Read]
        location: Optional[Location.Read]
        size: Optional[Size.Read]
        product: Optional[Product.Read]

        sender_details: Optional[str]


class ReservationSettings(SQLModel, table=True):
    __tablename__ = "reservation_settings"
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
    id_org: UUID = Field(foreign_key="org.id")

    max_rental_time: int
    max_rental_time_period: ResTimeUnit

    max_reservation_time: int
    max_reservation_time_period: ResTimeUnit

    transaction_buffer_time: int
    transaction_buffer_time_period: Optional[ResTimeUnit]
    locker_buffer_time: int
    locker_buffer_time_period: Optional[ResTimeUnit]

    class Write(BaseModel):
        max_rental_time: conint(ge=0)
        max_rental_time_period: ResTimeUnit

        max_reservation_time: conint(ge=0)

        max_reservation_time_period: ResTimeUnit

        transaction_buffer_time: conint(ge=0)
        transaction_buffer_time_period: Optional[ResTimeUnit]

        locker_buffer_time: conint(ge=0)
        locker_buffer_time_period: Optional[ResTimeUnit]

    class Read(BaseModel):
        id: UUID
        max_rental_time: conint(ge=0)
        max_rental_time_period: ResTimeUnit

        max_reservation_time: conint(ge=0)
        max_reservation_time_period: ResTimeUnit

        transaction_buffer_time: conint(ge=0)
        transaction_buffer_time_period: Optional[ResTimeUnit]

        locker_buffer_time: conint(ge=0)
        locker_buffer_time_period: Optional[ResTimeUnit]


class PaginatedReservation(BaseModel):
    items: list[Reservation.Read]

    total: int
    pages: int
