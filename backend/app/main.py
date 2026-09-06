from fastapi import FastAPI
from sqlalchemy import text

from .config import configure_cors
from .database import engine
from .exceptions import register_error_handlers
from .routers import consultation, diagnosis

app = FastAPI(title="ClinicCare Mini EMR API")

configure_cors(app)
register_error_handlers(app)

app.include_router(diagnosis.router)
app.include_router(consultation.router)


@app.get("/health")
def health_check():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}
