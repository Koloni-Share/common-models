from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from common_models.models.device.model import HardwareType, Mode
from pydantic import BaseModel, conint, constr
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel
from sqlmodel.sql.sqltypes import GUID
from common_models.util.form import as_form

if TYPE_CHECKING:
    from common_models.models.financial.model import StripeCountry
    from common_models.models.location.model import Location
    from common_models.models.price.model import Currency


class ResTimeUnit(Enum):
    minute = "minute"
    hour = "hour"
    day = "day"
    week = "week"


class DefaultNotification(Enum):
    sms = "sms"
    email = "email"


class ExpirationUnit(Enum):
    hours = "hours"
    days = "days"


class SignInMethod(Enum):
    email = "email"
    phone = "phone"
    both = "both"


class Language(Enum):
    en = "en"
    es = "es"
    it = "it"
    fr = "fr"
    pl = "pl"
    de = "de"


class OrgSettings(SQLModel, table=True):
    __tablename__ = "org_settings"
    __table_args__ = {"extend_existing": True}

    id: UUID = Field(primary_key=True)
    id_org: UUID = Field(foreign_key="org.id")

    default_country: Optional[StripeCountry]
    default_currency: Currency
    default_max_reservations: Optional[int]
    maintenance_on_issue: Optional[bool]

    parcel_expiration: Optional[int]
    parcel_expiration_unit: Optional[ExpirationUnit]
    use_long_parcel_codes: Optional[bool]

    default_time_zone: Optional[str]
    default_date_format: Optional[str]
    delivery_sms_start: Optional[str]
    service_sms_start: Optional[str]
    service_sms_charge: Optional[str]
    service_sms_end: Optional[str]
    event_sms_refund: Optional[str]

    invoice_prefix: Optional[str]

    default_device_hardware: Optional[HardwareType]
    default_device_mode: Optional[Mode]

    default_id_size: Optional[UUID] = Field(foreign_key="size.id")
    default_notification: Optional[DefaultNotification]
    default_notification_email: Optional[str]
    default_notification_phone: Optional[str]

    default_id_price: Optional[UUID] = Field(foreign_key="price.id")
    default_support_email: Optional[str] = "support@koloni.me"
    default_support_phone: Optional[str] = "+18337081205"

    language: Optional[str]

    # New contact for notifications
    new_contact_notification_enabled: Optional[bool]
    new_contact_notification_email_verified: Optional[bool]
    new_contact_notification_email: Optional[str]

    @as_form
    class Write(BaseModel):
        default_currency: Optional[Currency] = Currency.usd
        default_country: Optional[StripeCountry]
        default_max_reservations: Optional[int]
        maintenance_on_issue: Optional[bool] = True

        parcel_expiration: Optional[conint(gt=0)]
        parcel_expiration_unit: Optional[ExpirationUnit]
        use_long_parcel_codes: Optional[bool] = True

        default_time_zone: Optional[str]
        default_date_format: Optional[str]
        delivery_sms_start: Optional[str]
        service_sms_start: Optional[str]
        service_sms_charge: Optional[str]
        service_sms_end: Optional[str]
        event_sms_refund: Optional[str]

        invoice_prefix: Optional[
            constr(
                max_length=3,
                to_upper=True,
                strip_whitespace=True,
                regex=r"^[A-Z]+$",
            )
        ]

        default_device_hardware: Optional[HardwareType]
        default_device_mode: Optional[Mode]
        default_id_size: Optional[UUID]

        default_notification: Optional[DefaultNotification]
        default_notification_email: Optional[str]
        default_notification_phone: Optional[str]

        default_id_price: Optional[UUID]
        default_support_email: Optional[str] = "support@koloni.me"
        default_support_phone: Optional[str] = "+18337081205"

        language: Optional[Language] = Language.en

        # New contact for notifications
        new_contact_notification_enabled: Optional[bool]
        new_contact_notification_email: Optional[str]
        new_contact_notification_email_verified: Optional[bool]

    class Read(BaseModel):
        id: UUID
        id_org: UUID
        default_country: Optional[StripeCountry]
        default_currency: Currency
        default_max_reservations: Optional[int]
        maintenance_on_issue: Optional[bool]

        parcel_expiration: Optional[int]
        parcel_expiration_unit: Optional[ExpirationUnit]
        use_long_parcel_codes: Optional[bool]

        default_time_zone: Optional[str]
        default_date_format: Optional[str]
        delivery_sms_start: Optional[str]
        service_sms_start: Optional[str]
        service_sms_charge: Optional[str]
        service_sms_end: Optional[str]
        event_sms_refund: Optional[str]

        invoice_prefix: Optional[str]

        default_device_hardware: Optional[HardwareType]
        default_device_mode: Optional[Mode]
        default_id_size: Optional[UUID]

        default_notification: Optional[DefaultNotification]
        default_notification_email: Optional[str]
        default_notification_phone: Optional[str]

        default_id_price: Optional[UUID]
        default_support_email: Optional[str]  # new
        default_support_phone: Optional[str]  # new

        language: Optional[str]

        # New contact for notifications
        new_contact_notification_enabled: Optional[bool]
        new_contact_notification_email: Optional[str]
        new_contact_notification_email_verified: Optional[bool]


class LiteAppSettings(SQLModel, table=True):
    __tablename__ = "lite_app_settings"
    __table_args__ = {"extend_existing": True}

    id: UUID = Field(primary_key=True)
    id_org: UUID = Field(foreign_key="org.id")

    sign_in_method: Optional[SignInMethod]

    allow_multiple_rentals: Optional[bool]
    allow_user_reservation: Optional[bool]
    track_product_condition: Optional[bool]
    allow_photo_end_rental: Optional[bool]
    setup_in_app_payment: Optional[bool]

    primary_color: Optional[str]
    secondary_color: Optional[str]

    class Write(BaseModel):
        sign_in_method: Optional[SignInMethod]

        allow_multiple_rentals: Optional[bool]
        allow_user_reservation: Optional[bool]
        track_product_condition: Optional[bool]
        allow_photo_end_rental: Optional[bool]
        setup_in_app_payment: Optional[bool]

        primary_color: Optional[str] = "#ffffff"
        secondary_color: Optional[str] = "#ffffff"

    class Read(BaseModel):
        sign_in_method: Optional[SignInMethod]

        allow_multiple_rentals: Optional[bool]
        allow_user_reservation: Optional[bool]
        track_product_condition: Optional[bool]
        allow_photo_end_rental: Optional[bool]
        setup_in_app_payment: Optional[bool]

        primary_color: Optional[str]
        secondary_color: Optional[str]


class ReservationWidgetSettings(SQLModel, table=True):
    __tablename__ = "reservation_widget_settings"
    __table_args__ = {"extend_existing": True}

    id: UUID = Field(primary_key=True)
    id_org: UUID = Field(foreign_key="org.id")

    primary_color: Optional[str]
    secondary_color: Optional[str]
    background_color: Optional[str]

    duration: Optional[int]
    duration_unit: Optional[ResTimeUnit]

    in_app_payment: Optional[bool]

    class Write(BaseModel):
        primary_color: Optional[str] = "#000000"
        secondary_color: Optional[str] = "#000000"
        background_color: Optional[str] = "#000000"

        duration: Optional[int] = 0
        duration_unit: Optional[ResTimeUnit] = ResTimeUnit.hour

        in_app_payment: Optional[bool] = True

    class Read(BaseModel):
        primary_color: Optional[str]
        secondary_color: Optional[str]
        background_color: Optional[str]

        duration: Optional[int]
        duration_unit: Optional[ResTimeUnit]

        in_app_payment: Optional[bool]


# Base Model with common fields
class KioskSettingsBase(SQLModel):
    # General Settings
    general_select_mode_of_app_asset: Optional[bool]
    general_select_mode_of_app_storage: Optional[bool]
    general_select_mode_of_app_delivery: Optional[bool]
    general_select_mode_of_app_vending: Optional[bool]
    general_app_title_image_type_location: Optional[bool]
    general_app_title_image_type_organization: Optional[bool]
    general_app_scanning_mode_default_camera: Optional[bool]
    general_app_scanning_mode_dc_scanner: Optional[bool]
    general_app_orientation_portrait: Optional[bool]
    general_app_orientation_landscape: Optional[bool]
    general_app_show_customer_support_contact: Optional[bool]
    general_app_enable_select_environment: Optional[bool]

    # Asset Settings
    asset_user_sign_up_type_pincode: Optional[bool]
    asset_user_sign_up_type_qrcode: Optional[bool]
    asset_user_sign_up_type_rfid: Optional[bool]
    asset_report_condition_at_start_of_transaction: Optional[bool]
    asset_report_condition_at_end_of_transaction: Optional[bool]
    asset_user_sign_in_at_return: Optional[bool]
    asset_user_sign_in_at_return_type_pincode: Optional[bool]
    asset_user_sign_in_at_return_up_type_qrcode: Optional[bool]
    asset_user_sign_in_at_return_up_type_rfid: Optional[bool]

    # Storage Settings
    storage_start_storage_by_otp_verification: Optional[bool]
    storage_otp_verification_type_phone_number: Optional[bool]
    storage_otp_verification_type_email: Optional[bool]
    storage_start_storage_by_pincode: Optional[bool]
    storage_pincode_verification_type_pincode: Optional[bool]
    storage_pincode_verification_type_qrcode: Optional[bool]
    storage_pincode_verification_type_phone_number: Optional[bool]
    storage_pincode_verification_type_email: Optional[bool]
    storage_allow_opening_locker_without_ending_transaction: Optional[bool]
    storage_allow_set_duration: Optional[bool]

    # Vending Settings
    vending_user_sign_up_type_pincode: Optional[bool]
    vending_user_sign_up_type_qrcode: Optional[bool]
    vending_user_sign_up_type_rfid: Optional[bool]

    # Delivery Settings
    delivery_start_delivery_by_search_users: Optional[bool]
    delivery_start_delivery_by_scan_barcode: Optional[bool]
    delivery_search_by_user_through_first_name: Optional[bool]
    delivery_search_by_user_through_last_name: Optional[bool]
    delivery_search_by_user_through_phone_number: Optional[bool]
    delivery_search_by_user_through_email_id: Optional[bool]
    delivery_search_by_user_through_user_id: Optional[bool]
    delivery_search_by_user_through_address: Optional[bool]
    delivery_allow_access_to_order_id: Optional[bool]
    delivery_verify_user_pickup: Optional[bool]
    delivery_verify_user_pickup_type_pincode: Optional[bool]
    delivery_verify_user_pickup_type_signature: Optional[bool]
    delivery_access_driver_to_add_user: Optional[bool]


# Main Model with Table Definition
class KioskSettings(KioskSettingsBase, table=True):
    __tablename__ = "kiosk_settings"
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
    id_org: UUID = Field(nullable=False)
    location_id: UUID = Field(foreign_key="location.id", nullable=False)

    created_at: datetime = Field(
        sa_column=Column(
            "created_at",
            DateTime(timezone=True),
            server_default=func.current_timestamp(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            "updated_at",
            DateTime(timezone=True),
            server_default=func.current_timestamp(),
            onupdate=func.current_timestamp(),
            nullable=False,
        )
    )


# Read Model
class KioskSettingsRead(KioskSettingsBase):
    id: UUID
    id_org: UUID
    location: Location.Read
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Write Model
class KioskSettingsWrite(KioskSettingsBase):
    id_org: UUID
    location_id: UUID
