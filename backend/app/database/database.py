from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# ---------------------------------------------------------
# Database location
# ---------------------------------------------------------

# backend/
BASE_DIR = Path(__file__).resolve().parents[2]

# The database will be created here:
# backend/telemetry.db
DATABASE_PATH = BASE_DIR / "telemetry.db"


# SQLite connection string
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"


# ---------------------------------------------------------
# SQLAlchemy engine
# ---------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


# ---------------------------------------------------------
# Session factory
# ---------------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ---------------------------------------------------------
# Declarative Base
# ---------------------------------------------------------

Base = declarative_base()