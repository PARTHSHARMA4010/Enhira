from sqlmodel import create_engine, Session
import os

db_url = os.getenv("DB_URL", "sqlite:///./test.db")   # uses SQLite for now
engine = create_engine(db_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
