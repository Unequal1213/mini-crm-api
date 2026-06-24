from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.deal import (
    DealCreate,
    DealResponse,
    DealSortBy,
    DealStage,
    DealStatsResponse,
    DealUpdate,
    SortOrder,
)
from app.services import deals as deal_service

router = APIRouter(prefix="/deals", tags=["deals"])

DbSession = Annotated[Session, Depends(get_db)]
Limit = Annotated[int, Query(ge=1, le=100)]
Offset = Annotated[int, Query(ge=0)]
NonNegativeDecimal = Annotated[Decimal, Query(ge=0)]


@router.post("", response_model=DealResponse, status_code=status.HTTP_201_CREATED)
def create_deal(deal_data: DealCreate, db: DbSession) -> DealResponse:
    deal = deal_service.create_deal(db, deal_data)
    if deal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return deal


@router.get("", response_model=list[DealResponse])
def list_deals(
    db: DbSession,
    limit: Limit = 20,
    offset: Offset = 0,
    stage: DealStage | None = None,
    customer_id: int | None = None,
    source: str | None = None,
    min_value: NonNegativeDecimal | None = None,
    max_value: NonNegativeDecimal | None = None,
    sort_by: DealSortBy = "created_at",
    sort_order: SortOrder = "desc",
) -> list[DealResponse]:
    return deal_service.list_deals(
        db,
        limit=limit,
        offset=offset,
        stage=stage,
        customer_id=customer_id,
        source=source,
        min_value=min_value,
        max_value=max_value,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get("/stats", response_model=DealStatsResponse)
def get_deal_stats(db: DbSession) -> DealStatsResponse:
    return deal_service.get_deal_stats(db)


@router.get("/{deal_id}", response_model=DealResponse)
def get_deal(deal_id: int, db: DbSession) -> DealResponse:
    deal = deal_service.get_deal(db, deal_id)
    if deal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found",
        )
    return deal


@router.patch("/{deal_id}", response_model=DealResponse)
def update_deal(
    deal_id: int,
    deal_data: DealUpdate,
    db: DbSession,
) -> DealResponse:
    deal = deal_service.get_deal(db, deal_id)
    if deal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found",
        )

    updated_deal = deal_service.update_deal(db, deal, deal_data)
    if updated_deal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return updated_deal


@router.delete("/{deal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_deal(deal_id: int, db: DbSession) -> Response:
    deal = deal_service.get_deal(db, deal_id)
    if deal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found",
        )

    deal_service.delete_deal(db, deal)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
