from fastapi import FastAPI

app = FastAPI(title="ClinicCare Mini EMR API")


@app.get("/health")
def health_check():
    return {"status": "ok"}
