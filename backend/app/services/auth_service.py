import os
import hmac
import hashlib
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.schemas.auth import User

SECRET_KEY = os.getenv(
    "MISSIONVAULT_SECRET_KEY",
    "change-this-secret-key"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("MISSIONVAULT_TOKEN_EXPIRE_MINUTES", "1440")
)

DEMO_USERNAME = os.getenv(
    "MISSIONVAULT_DEMO_USERNAME",
    "operator"
)

DEMO_PASSWORD = os.getenv(
    "MISSIONVAULT_DEMO_PASSWORD",
    "SpaceDogs2026"
)

# Demo-only static salt. Good enough for this internal project phase.
PASSWORD_SALT = os.getenv(
    "MISSIONVAULT_PASSWORD_SALT",
    "missionvault-demo-salt"
)

security = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    """Return a deterministic PBKDF2 hash."""
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        PASSWORD_SALT.encode("utf-8"),
        100_000
    )
    return digest.hex()


def verify_password(plain_password: str, stored_hash: str) -> bool:
    """Compare password hashes safely."""
    computed_hash = hash_password(plain_password)
    return hmac.compare_digest(computed_hash, stored_hash)


_DEMO_USER = {
    "username": DEMO_USERNAME,
    "full_name": "Mission Operator",
    "disabled": False,
    "hashed_password": hash_password(DEMO_PASSWORD)
}


def authenticate_user(username: str, password: str) -> User | None:
    if username != _DEMO_USER["username"]:
        return None

    if not verify_password(password, _DEMO_USER["hashed_password"]):
        return None

    return User(
        username=_DEMO_USER["username"],
        full_name=_DEMO_USER["full_name"],
        disabled=_DEMO_USER["disabled"]
    )


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username != _DEMO_USER["username"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return User(
            username=_DEMO_USER["username"],
            full_name=_DEMO_USER["full_name"],
            disabled=_DEMO_USER["disabled"]
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )