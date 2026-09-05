from fastapi import FastAPI
from sqlalchemy import text

from .database import engine
from .routers import diagnosis

app = FastAPI(title="ClinicCare Mini EMR API")

app.include_router(diagnosis.router)


@app.get("/health")
def health_check():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}
