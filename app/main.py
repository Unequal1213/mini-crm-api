from fastapi import FastAPI

from app.api.customers import router as customers_router

app = FastAPI(title="Mini CRM API")

app.include_router(customers_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
