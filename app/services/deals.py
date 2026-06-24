from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Customer, Deal
from app.schemas.deal import DealCreate, DealUpdate


def create_deal(db: Session, deal_data: DealCreate) -> Deal | None:
    customer = db.get(Customer, deal_data.customer_id)
    if customer is None:
        return None

    deal = Deal(**deal_data.model_dump())
    db.add(deal)
    db.commit()
    db.refresh(deal)
    return deal


def list_deals(db: Session) -> list[Deal]:
    result = db.scalars(select(Deal).order_by(Deal.id))
    return list(result.all())


def get_deal(db: Session, deal_id: int) -> Deal | None:
    return db.get(Deal, deal_id)


def update_deal(
    db: Session,
    deal: Deal,
    deal_data: DealUpdate,
) -> Deal | None:
    data = deal_data.model_dump(exclude_unset=True)
    customer_id = data.get("customer_id")
    if customer_id is not None and db.get(Customer, customer_id) is None:
        return None

    for field, value in data.items():
        setattr(deal, field, value)

    db.commit()
    db.refresh(deal)
    return deal


def delete_deal(db: Session, deal: Deal) -> None:
    db.delete(deal)
    db.commit()
