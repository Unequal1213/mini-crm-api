from fastapi import FastAPI

from app.api.customers import router as customers_router
from app.api.deals import router as deals_router

app = FastAPI(title="Mini CRM API")

app.include_router(customers_router)
app.include_router(deals_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
