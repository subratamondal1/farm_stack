from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./finance.db"

ENGINE = create_engine(
    url=DATABASE_URL,
    connect_args={"check_same_thread":False}
)

SessionLocal = sessionmaker(
    bind=ENGINE,
    autoflush=False,
    autocommit=False
)

BASE = declarative_base()