from fastapi import FastAPI
from sqlalchemy import text

from .database import engine
from .exceptions import register_error_handlers
from .routers import diagnosis

app = FastAPI(title="ClinicCare Mini EMR API")

register_error_handlers(app)

app.include_router(diagnosis.router)


@app.get("/health")
def health_check():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}
