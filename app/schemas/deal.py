from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

DealStage = Literal["lead", "qualified", "proposal", "won", "lost"]
DealSortBy = Literal[
    "expected_close_date",
    "created_at",
    "updated_at",
    "value",
    "title",
    "stage",
    "source",
]
SortOrder = Literal["asc", "desc"]


class DealCreate(BaseModel):
    customer_id: int
    title: str = Field(min_length=1, max_length=255)
    value: Decimal = Field(ge=0)
    stage: DealStage
    source: str | None = Field(default=None, max_length=100)
    notes: str | None = None
    expected_close_date: date | None = None


class DealUpdate(BaseModel):
    customer_id: int | None = None
    title: str | None = Field(default=None, min_length=1, max_length=255)
    value: Decimal | None = Field(default=None, ge=0)
    stage: DealStage | None = None
    source: str | None = Field(default=None, max_length=100)
    notes: str | None = None
    expected_close_date: date | None = None


class DealResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    title: str
    value: Decimal
    stage: DealStage
    source: str | None
    notes: str | None
    expected_close_date: date | None
    created_at: datetime
    updated_at: datetime
