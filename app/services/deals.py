from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Customer, Deal
from app.schemas.deal import DealCreate, DealSortBy, DealStage, DealUpdate, SortOrder

OPEN_STAGES = {"lead", "qualified", "proposal"}


def create_deal(db: Session, deal_data: DealCreate) -> Deal | None:
    customer = db.get(Customer, deal_data.customer_id)
    if customer is None:
        return None

    deal = Deal(**deal_data.model_dump())
    db.add(deal)
    db.commit()
    db.refresh(deal)
    return deal


def list_deals(
    db: Session,
    *,
    limit: int = 20,
    offset: int = 0,
    stage: DealStage | None = None,
    customer_id: int | None = None,
    source: str | None = None,
    min_value: Decimal | None = None,
    max_value: Decimal | None = None,
    sort_by: DealSortBy = "created_at",
    sort_order: SortOrder = "desc",
) -> list[Deal]:
    statement = select(Deal)

    if stage is not None:
        statement = statement.where(Deal.stage == stage)
    if customer_id is not None:
        statement = statement.where(Deal.customer_id == customer_id)
    if source is not None:
        statement = statement.where(Deal.source == source)
    if min_value is not None:
        statement = statement.where(Deal.value >= min_value)
    if max_value is not None:
        statement = statement.where(Deal.value <= max_value)

    sort_column = getattr(Deal, sort_by)
    sort_expression = sort_column.asc() if sort_order == "asc" else sort_column.desc()
    id_tiebreaker = Deal.id.asc() if sort_order == "asc" else Deal.id.desc()
    statement = statement.order_by(sort_expression, id_tiebreaker).offset(offset).limit(
        limit,
    )

    result = db.scalars(statement)
    return list(result.all())


def get_deal(db: Session, deal_id: int) -> Deal | None:
    return db.get(Deal, deal_id)


def get_deal_stats(db: Session) -> dict[str, int | float]:
    deals = db.scalars(select(Deal)).all()
    stats: dict[str, int | float] = {
        "total": 0,
        "lead": 0,
        "qualified": 0,
        "proposal": 0,
        "won": 0,
        "lost": 0,
        "total_value": 0,
        "won_value": 0,
        "open_value": 0,
    }

    total_value = Decimal("0")
    won_value = Decimal("0")
    open_value = Decimal("0")

    for deal in deals:
        stats["total"] += 1
        stats[deal.stage] += 1
        total_value += deal.value

        if deal.stage == "won":
            won_value += deal.value
        if deal.stage in OPEN_STAGES:
            open_value += deal.value

    stats["total_value"] = float(total_value)
    stats["won_value"] = float(won_value)
    stats["open_value"] = float(open_value)
    return stats


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
