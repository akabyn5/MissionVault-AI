from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base, engine

# Import this so SQLAlchemy registers the model
# before create_all() runs.
from app.models.telemetry import TelemetryRecord

from app.routers.telemetry import router as telemetry_router


# ---------------------------------------------------------
# Create database tables
# ---------------------------------------------------------

Base.metadata.create_all(
    bind=engine
)


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="MissionVault AI API",
    description=(
        "Backend API for secure satellite telemetry "
        "and anomaly detection"
    ),
    version="0.1.0"
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ],
)


# ---------------------------------------------------------
# Include telemetry routes
# ---------------------------------------------------------

app.include_router(
    telemetry_router
)


# ---------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------

@app.get("/")
def root():

    return {
        "message": (
            "MissionVault AI Backend Running"
        ),
        "version": "0.1.0"
    }