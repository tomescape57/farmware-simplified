from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base #orm: object relational mapper


SQLALCHEMY_DATABASE_URL = "sqlite:///./farmware.db" #SQLAlchemy's specific format of url. Create/Connect to a SQLite database file named farmware.db located in the current working directory.

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} # Required for SQLite, FastAPI handles multiple requests simultaneously (using threads/async).
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# This dependency will be used in routers 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()