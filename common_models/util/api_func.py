from typing import Any

from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from pydantic import BaseModel, Field
from sqlalchemy import VARCHAR, cast


class PaginationInfo(BaseModel):
    total: int = Field(default=0, description="Total number of items.")
    page: int = Field(default=1, description="Current page number.")
    page_size: int = Field(default=10, description="Number of items per page.")
    total_pages: int = Field(default=1, description="Total number of pages.")


async def _get_by_key_value(key: str, value: str, model: Any) -> Any:
    if key not in model.__table__.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field: {key}",
        )

    query = query.filter(cast(model.__table__.columns[key], VARCHAR) == value)

    result = await db.session.execute(query)
    model = result.unique().scalar_one()


async def _get_paginated_query(
    results: Any, page: int, size: int
) -> tuple[PaginationInfo, list[Any]]:
    """
    Paginate results
    """
    total = len(results)
    total_pages = (total + size - 1) // size

    paginated_results = results[(page - 1) * size : page * size]

    pagination_info = PaginationInfo(
        total=total, page=page, page_size=size, total_pages=total_pages
    )
    return pagination_info, paginated_results
