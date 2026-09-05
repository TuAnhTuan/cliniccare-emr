from fastapi import FastAPI
from sqlalchemy import text

from .database import engine

app = FastAPI(title="ClinicCare Mini EMR API")


@app.get("/health")
def health_check():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}
