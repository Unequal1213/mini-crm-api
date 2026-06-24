from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.deal import DealCreate, DealResponse, DealUpdate
from app.services import deals as deal_service

router = APIRouter(prefix="/deals", tags=["deals"])

DbSession = Annotated[Session, Depends(get_db)]


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
def list_deals(db: DbSession) -> list[DealResponse]:
    return deal_service.list_deals(db)


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
