import importlib
import sys
from types import ModuleType

import pytest


def import_model_modules(monkeypatch: pytest.MonkeyPatch) -> tuple[
    ModuleType,
    ModuleType,
    ModuleType,
]:
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg://username:password@localhost:5432/test_db",
    )

    for module_name in (
        "app.models.deal",
        "app.models.customer",
        "app.database.database",
    ):
        sys.modules.pop(module_name, None)

    database_module = importlib.import_module("app.database.database")
    customer_module = importlib.import_module("app.models.customer")
    deal_module = importlib.import_module("app.models.deal")

    return database_module, customer_module, deal_module


def test_customer_and_deal_tables_are_registered(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database_module, _, _ = import_model_modules(monkeypatch)

    assert "customers" in database_module.Base.metadata.tables
    assert "deals" in database_module.Base.metadata.tables


def test_customer_deal_relationship_is_configured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, customer_module, deal_module = import_model_modules(monkeypatch)

    assert customer_module.Customer.deals.property.mapper.class_ is deal_module.Deal
    assert deal_module.Deal.customer.property.mapper.class_ is customer_module.Customer
