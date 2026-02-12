from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from Backend.env_helper import env

DATABASE_URL = (
    f"mysql+pymysql://{env('DB_USER')}:"
    f"{env('DB_PASSWORD')}@"
    f"{env('DB_HOST')}:"
    f"{env('DB_PORT')}/"
    f"{env('DB_NAME')}"
)
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()