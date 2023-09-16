from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..core.config import settings

# Database URL from the config file
DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

# Create an engine. The `echo` flag is a shortcut to setting up SQLAlchemy logging, useful for debugging.
engine = create_engine(DATABASE_URL, echo=True)

# Create a local session factory. This factory will be used to create individual sessions throughout the app.
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Dependency to get DB session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
