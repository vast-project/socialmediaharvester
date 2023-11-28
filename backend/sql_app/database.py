from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

# da salvare i dati del db in un file di configurazione
from settings import SQLALCHEMY_DATABASE_URL

"""The first step is to create a SQLAlchemy "engine".
We will later use this engine in other places."""
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# connessione al db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
