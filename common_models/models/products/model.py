from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from common_models.models.device.model import Device
from pydantic import BaseModel, condecimal, constr
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID
from common_models.util.form import as_form

if TYPE_CHECKING:
    from common_models.models.conditions.link_product_condition import ConditionProductLink
    from common_models.models.product_tracking.product_tracking import ProductTracking
    from common_models.models.products.condition import ProductCondition
    from common_models.models.conditions.model import Condition


class Product(SQLModel, table=True):
    __tablename__ = "product"
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

    image: Optional[str]
    name: str
    description: Optional[str]

    price: condecimal(max_digits=8, decimal_places=2, gt=0)
    sales_price: Optional[condecimal(max_digits=8, decimal_places=2, gt=0)]
    sku: Optional[str]
    msrp: Optional[str]
    serial_number: Optional[str]

    id_condition: Optional[UUID] = Field(foreign_key="condition.id")
    condition: ProductCondition = ProductCondition.new

    possible_conditions: list["Condition"] = Relationship(
        back_populates="products",
        link_model=ConditionProductLink,
        sa_relationship_kwargs={"lazy": "joined", "join_depth": 1},
    )

    repair_on_broken: bool = False
    report_on_broken: bool = False

    id_org: UUID = Field(foreign_key="org.id")
    id_product_group: Optional[UUID] = Field(foreign_key="product_group.id")

    devices: list["Device"] = Relationship(
        back_populates="product",
        sa_relationship_kwargs={"lazy": "joined", "join_depth": 1},
    )

    product_group: Optional["ProductGroup"] = Relationship(  # noqa: F821
        back_populates="products",
        sa_relationship_kwargs={"lazy": "noload"},
    )

    product_tracking: list["ProductTracking"] = Relationship(
        back_populates="product",
        # sa_relationship_kwargs={"lazy": "joined", "join_depth": 1},
    )

    reservation: Optional["Reservation"] = Relationship(  # noqa: F821
        back_populates="product",
        sa_relationship_kwargs={
            "lazy": "noload",
            "uselist": False,
        },
    )

    @as_form
    class Write(BaseModel):
        name: str
        description: Optional[str]
        price: Optional[condecimal(max_digits=8, decimal_places=2, gt=0)]
        sales_price: Optional[condecimal(max_digits=8, decimal_places=2, gt=0)]
        sku: Optional[str] = ""
        msrp: Optional[str] = ""
        serial_number: Optional[constr(strip_whitespace=True)]
        condition: ProductCondition = ProductCondition.new
        id_condition: Optional[UUID] = None
        repair_on_broken: Optional[bool] = False
        report_on_broken: Optional[bool] = False
        id_product_group: Optional[UUID] = None

    class Patch(BaseModel):
        name: Optional[str]
        price: Optional[condecimal(max_digits=8, decimal_places=2, gt=0)]
        description: Optional[str]
        sku: Optional[str]
        msrp: Optional[str]
        serial_number: Optional[str]
        condition: Optional[ProductCondition]
        id_condition: Optional[UUID] = None
        repair_on_broken: Optional[bool]
        report_on_broken: Optional[bool]
        id_product_group: Optional[UUID] = None

    class Read(BaseModel):
        id: UUID
        created_at: datetime

        image: Optional[str]
        name: str
        description: Optional[str]
        price: Optional[condecimal(max_digits=8, decimal_places=2, gt=0)]
        sales_price: Optional[condecimal(max_digits=8, decimal_places=2, gt=0)]
        sku: Optional[str]
        msrp: Optional[str]
        serial_number: Optional[str]
        condition: ProductCondition
        repair_on_broken: bool
        report_on_broken: bool
        id_product_group: Optional[UUID] = None
        id_condition: Optional[UUID]

        devices: Optional[list[Device.Read]]

        product_tracking: Optional[list[ProductTracking.Read]]
        possible_conditions: Optional[List]


class PaginatedProducts(BaseModel):
    items: list[Product.Read]
    total: int
    pages: int
