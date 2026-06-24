from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


def create_customer(db: Session, customer_data: CustomerCreate) -> Customer:
    data = customer_data.model_dump()

    customer = Customer(**data)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def list_customers(db: Session) -> list[Customer]:
    result = db.scalars(select(Customer).order_by(Customer.id))
    return list(result.all())


def get_customer(db: Session, customer_id: int) -> Customer | None:
    return db.get(Customer, customer_id)


def update_customer(
    db: Session,
    customer: Customer,
    customer_data: CustomerUpdate,
) -> Customer:
    data = customer_data.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer: Customer) -> None:
    db.delete(customer)
    db.commit()
