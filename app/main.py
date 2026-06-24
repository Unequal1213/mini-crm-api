from fastapi import FastAPI

app = FastAPI(title="Mini CRM API")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
