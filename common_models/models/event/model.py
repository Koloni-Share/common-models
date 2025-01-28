from datetime import datetime
from decimal import Decimal
from enum import Enum, StrEnum
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from common_models.models.device.model import Device
from fastapi import HTTPException, Request
from pydantic import AnyHttpUrl, AnyUrl, BaseModel, condecimal, conint, constr
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID

if TYPE_CHECKING:
    from common_models.models.memberships.model import Membership
    from common_models.models.promo.model import Promo
    from common_models.models.reservations.model import Reservation
    from common_models.models.user.model import User


class EventResponse(BaseModel):
    id_event: UUID
    event_status: str
    started_at: datetime
    ended_at: datetime | None = None
    canceled_at: datetime | None = None
    invoice_id: str | None = None
    order_id: str | None = None
    id_user: UUID | None = None
    id_device: UUID | None = None
    device_status: str | None = None
    courier_pin_code: str | None = None
    access_code: str | None = None
    tracking_number: str | None = None
    total: Decimal | None = None
    refunded_amount: Decimal | None = Field(default=Decimal('0.00'))
    signature_url: str | None = None
    image_url: AnyUrl | None = None
    penalize_charge: float | None = None
    penalize_reason: str | None = None

    @property
    def id(self) -> UUID:
        return self.id_event


class EventStatus(Enum):
    in_progress = "in_progress"
    awaiting_payment_confirmation = "awaiting_payment_confirmation"
    awaiting_service_pickup = "awaiting_service_pickup"
    awaiting_service_dropoff = "awaiting_service_dropoff"
    awaiting_user_pickup = "awaiting_user_pickup"
    transaction_in_progress = "transaction_in_progress"
    finished = "finished"
    canceled = "canceled"
    refunded = "refunded"
    reserved = "reserved"
    expired = "expired"


ACTIVE_EVENT_STATUSES = [
    EventStatus.expired,
    EventStatus.in_progress,
    EventStatus.transaction_in_progress,
    EventStatus.awaiting_payment_confirmation,
    EventStatus.awaiting_service_pickup,
    EventStatus.awaiting_service_dropoff,
    EventStatus.awaiting_user_pickup,
]


class PenalizeReason(Enum):
    missing_items = "missing_items"
    damaged_items = "damaged_items"
    misconduct = "misconduct"
    other = "other"


class EventType(Enum):
    service = "service"
    rental = "rental"
    storage = "storage"
    delivery = "delivery"
    vending = "vending"


class AppType(Enum):
    mobile = "mobile"
    web = "web"


class Duration(BaseModel):
    hours: Optional[conint(ge=0)] = 0
    days: Optional[conint(ge=0)] = 0
    weeks: Optional[conint(ge=0)] = 0


class PublicEvent(BaseModel):
    id: UUID
    app_logo: Optional[str]
    invoice_id: Optional[str]
    created_at: datetime

    event_status: EventStatus
    event_type: EventType

    device_name: str
    device_id: UUID
    device_number: Optional[int]
    location_name: str
    location_address: str
    user_phone: Optional[str]
    user_email: Optional[str]
    user_name: Optional[str]


class BatchResponse(BaseModel):
    status_code: int
    event_code: int
    response: dict | str


class Event(SQLModel, table=True):
    __tablename__ = "event"
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

    started_at: datetime = Field(
        sa_column=Column("started_at", DateTime(timezone=True))
    )

    ended_at: datetime = Field(sa_column=Column("ended_at", DateTime(timezone=True)))
    canceled_at: Optional[datetime] = Field(
        sa_column=Column("canceled_at", DateTime(timezone=True))
    )

    invoice_id: str = Field(nullable=True)
    order_id: Optional[str] = Field(nullable=True)

    # Stripe
    payment_intent_id: str = Field(nullable=True)
    setup_intent_id: str = Field(nullable=True)
    stripe_subscription_id: str = Field(nullable=True)

    # Harbor Specific
    harbor_session_seed: str = Field(nullable=True)
    harbor_session_token: str = Field(nullable=True)
    harbor_session_token_auth: str = Field(nullable=True)
    harbor_payload: str = Field(nullable=True)
    harbor_payload_auth: str = Field(nullable=True)
    harbor_reservation_id: str = Field(nullable=True)

    # Delivery Only
    code: Optional[int] = Field(nullable=True)

    # Passcode
    passcode: Optional[constr(regex=r"\d{4}", max_length=4, min_length=4)] = Field(
        nullable=True
    )

    event_status: EventStatus = Field(default=EventStatus.in_progress)
    event_type: EventType = Field(default=EventType.service)

    total: condecimal(max_digits=8, decimal_places=2) = Field(nullable=True)
    total_time: str = Field(nullable=True)
    weight: Optional[float]

    refunded_amount: condecimal(max_digits=8, decimal_places=2) = 0

    penalize_charge: Optional[float]
    penalize_reason: Optional[PenalizeReason]

    signature_url: Optional[str] = Field(nullable=True)

    courier_pin_code: Optional[str]
    canceled_by: Optional[str]  # Member's name
    image_url: Optional[AnyHttpUrl] = Field(nullable=True)

    id_org: UUID = Field(foreign_key="org.id")
    id_user: Optional[UUID] = Field(foreign_key="User.id")
    id_device: UUID = Field(foreign_key="device.id")
    id_promo: Optional[UUID] = Field(foreign_key="promo.id")
    id_membership: Optional[UUID] = Field(foreign_key="memberships.id")

    device: Optional["Device"] = Relationship(
        back_populates="events",
        sa_relationship_kwargs={"lazy": "joined", "uselist": False},
    )

    user: Optional["User"] = Relationship(
        back_populates="events",
        sa_relationship_kwargs={"lazy": "joined", "uselist": False},
    )

    promo: Optional["Promo"] = Relationship(
        back_populates="events",
        sa_relationship_kwargs={"lazy": "joined", "uselist": False},
    )

    membership: Optional["Membership"] = Relationship(
        back_populates="events",
        sa_relationship_kwargs={"lazy": "joined", "uselist": False},
    )

    issue: Optional["Issue"] = Relationship(  # noqa: F821
        back_populates="event",
        sa_relationship_kwargs={"lazy": "noload", "uselist": False},
    )

    log: Optional["Log"] = Relationship(  # noqa: F821
        back_populates="event",
        sa_relationship_kwargs={"lazy": "noload", "uselist": False},
    )

    # Notification Status
    notification_status: Optional[str] = Field(nullable=True)
    notification_status_date: Optional[datetime] = Field(
        nullable=True,
        sa_column=Column("notification_status_date", DateTime(timezone=True)),
    )

    class Read(BaseModel):
        id: UUID
        invoice_id: Optional[str]
        order_id: Optional[str]
        code: Optional[int]
        created_at: datetime
        started_at: Optional[datetime]
        ended_at: Optional[datetime]
        canceled_at: Optional[datetime]

        event_status: EventStatus
        event_type: EventType

        harbor_session_seed: Optional[str]
        harbor_session_token: Optional[str]
        harbor_session_token_auth: Optional[str]
        harbor_payload: Optional[str]
        harbor_payload_auth: Optional[str]
        harbor_reservation_id: Optional[str]

        image_url: Optional[AnyHttpUrl]

        total: Optional[float]
        total_time: Optional[str]
        weight: Optional[float]

        refunded_amount: Optional[float]

        penalize_charge: Optional[float]
        penalize_reason: Optional[PenalizeReason]

        courier_pin_code: Optional[str]
        canceled_by: Optional[str]  # Member's name

        signature_url: Optional[str]

        id_user: Optional[UUID]
        id_device: Optional[UUID]

        device: Optional[Device.Read]
        user: Optional[User.Read]
        promo: Optional[Promo.Read]
        membership: Optional[Membership.Read]

        notification_status: Optional[str]
        notification_status_date: Optional[datetime]


class EventBatch(BaseModel):
    detail: str
    items: list[Event.Read]
    err: Optional[list]


class PaginatedEvents(BaseModel):
    items: list[Event.Read]

    total: int
    pages: int


class StripeCustomerData(BaseModel):
    ephemeral_key: Optional[dict]
    customer_id: Optional[str]


class StripePaymentData(BaseModel):
    client_secret: Optional[str]
    customer_data: Optional[StripeCustomerData]
    publishable_key: Optional[str]


class StartReservationResponse(BaseModel):
    client_secret: Optional[str]
    customer_data: Optional[StripeCustomerData]
    publishable_key: Optional[str]
    stripe_account_id: Optional[str]

    # Event fields

    id: UUID
    invoice_id: Optional[str]
    order_id: Optional[str]
    code: Optional[str]
    created_at: datetime

    event_status: EventStatus
    event_type: EventType

    payment_intent_id: Optional[str]
    setup_intent_id: Optional[str]

    total: Optional[float]

    id_user: Optional[UUID]
    id_device: UUID


class CompleteReservationResponse(BaseModel):
    id: UUID
    redirect_url_3ds: Optional[str]
    invoice_id: Optional[str]
    order_id: Optional[str]
    code: Optional[int]
    created_at: datetime
    started_at: Optional[datetime]
    ended_at: Optional[datetime]

    event_status: EventStatus
    event_type: EventType

    harbor_session_seed: Optional[str]
    harbor_session_token: Optional[str]
    harbor_session_token_auth: Optional[str]
    harbor_payload: Optional[str]
    harbor_payload_auth: Optional[str]
    harbor_reservation_id: Optional[str]

    total: Optional[float]
    total_time: Optional[str]

    refunded_amount: Optional[float]

    id_user: Optional[UUID]
    id_device: UUID

    device: Optional[Device.Read]
    user: Optional[User.Read]


class StartEvent(BaseModel):
    event_type: EventType

    from_user: Optional[UUID]

    id_condition: Optional[UUID]
    id_device: Optional[UUID]

    id_size: Optional[UUID]
    size_external_id: Optional[str]
    id_location: Optional[UUID]
    location_external_id: Optional[str]

    order_id: Optional[str]

    id_user: Optional[UUID]
    user_external_id: Optional[str]
    phone_number: Optional[str]
    pin_code: Optional[constr(regex=r"\d{4}", max_length=4, min_length=4)]
    passcode: Optional[constr(regex=r"\d{4}", max_length=4, min_length=4)]
    duration: Optional[Duration]


class DeliveryInput(StartEvent):
    id_org: UUID
    reservation: Reservation | None = None
    tracking_number: str | None = None
    event_type: EventType = Field(default=EventType.delivery, const=True)
    size_external_id: Optional[str]

    async def fetch_reservation(self, id_org: UUID):
        from ..reservations.controller import get_reservation_by_tracking_number

        reservation = await get_reservation_by_tracking_number(self.order_id, id_org)
        if not reservation:
            raise HTTPException(
                status_code=404,
                detail=f"Invalid barcode. Please use another barcode to proceed.",
            )
        if not reservation.id_device:
            raise HTTPException(
                status_code=400,
                detail="No device was assigned to this reservation",
            )
        if self.id_location and self.id_location != reservation.id_location:
            raise HTTPException(
                status_code=400,
                detail="Reservation must be loaded at the location it was created for",
            )

        self.reservation = reservation
        self.tracking_number = reservation.tracking_number
        self.id_device = reservation.id_device
        self.id_user = reservation.id_user
        self.id_location = reservation.id_location


class ShareEventResponse(BaseModel):
    message: str
    sms_success: bool | None
    email_success: bool | None


class NotificationStatus(StrEnum):
    SENT = "sent"
    FAILED = "failed"
