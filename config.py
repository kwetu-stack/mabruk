import os
from datetime import datetime
from zoneinfo import ZoneInfo

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
NAIROBI_TZ = ZoneInfo("Africa/Nairobi")


def now_in_nairobi():
    return datetime.now(NAIROBI_TZ)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "alaskan-sales-2026")

    os.makedirs(INSTANCE_DIR, exist_ok=True)

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(INSTANCE_DIR, "alaskan.db")
    )

    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://",
            "postgresql+psycopg://",
            1,
        )
    elif SQLALCHEMY_DATABASE_URI.startswith("postgresql://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1,
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
