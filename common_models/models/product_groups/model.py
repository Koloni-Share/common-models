from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, constr, validator
from sqlalchemy import Column, DateTime, String, func
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel.sql.sqltypes import GUID
from common_models.util.form import as_form

from common_models.models.products.model import PaginatedProducts, Product
from common_models.models.size.model import Size


class ProductGroup(SQLModel, table=True):
    __tablename__ = "product_group"
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

    name: constr(min_length=3, max_length=100, strip_whitespace=True) = Field(
        sa_column=Column("name", String(100), nullable=False)
    )

    image: Optional[str] = Field(nullable=True)

    auto_repair: bool
    transaction_number: int  # auto repair after this number of transactions (if auto_repair is true)

    charging_time: int
    one_to_one: bool

    id_org: UUID = Field(foreign_key="org.id")
    id_size: Optional[UUID] = Field(foreign_key="size.id")

    total_inventory: int
    products: list["Product"] = Relationship(
        back_populates="product_group",
        sa_relationship_kwargs={"lazy": "joined"},
    )

    size: Optional["Size"] = Relationship(
        back_populates="product_groups",
        sa_relationship_kwargs={"lazy": "joined"},
    )

    @as_form
    class Write(BaseModel):
        name: constr(min_length=3, max_length=100, strip_whitespace=True)

        @validator("name")
        def validate_name(cls, value):
            if not value.isalnum():
                raise ValueError("The name must only contain alphanumeric characters.")
            return value

        auto_repair: Optional[bool] = False
        transaction_number: Optional[int] = 0
        charging_time: Optional[int] = 0
        one_to_one: Optional[bool] = False
        id_size: Optional[UUID] = None
        total_inventory: Optional[int] = 0
        products: Optional[list[UUID]] = []
        # image: Optional[str] = None

    class Patch(BaseModel):
        name: Optional[str]
        auto_repair: Optional[bool]
        transaction_number: Optional[int]
        charging_time: Optional[int]
        one_to_one: Optional[bool]
        total_inventory: int
        id_size: Optional[UUID] = None

    class Read(BaseModel):
        id: UUID
        created_at: datetime

        name: str
        image: Optional[str]
        auto_repair: bool
        transaction_number: int
        charging_time: int
        one_to_one: bool
        total_inventory: int
        products: Optional[list[Product.Read]]
        size: Optional[Size.Read]


class PaginatedProductGroups(BaseModel):
    items: list[ProductGroup.Read]
    total: int
    pages: int


class CombinedProductsGroupsResponse(BaseModel):
    total: int
    pages: int

    product_group: PaginatedProductGroups
    product_list: PaginatedProducts
