from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.config import DB_FILE

# Initialize Database
DATABASE_URL = f"sqlite:///{DB_FILE}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Model
class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hotel_name = Column(String, index=True)
    date = Column(String, index=True)
    provider = Column(String, index=True)
    price = Column(String)
    screenshot = Column(String)

# Initialize Database
def init_db():
    """Creates database tables."""
    Base.metadata.create_all(bind=engine)

# Save results to Database
def save_results(results: dict):
    """Stores test results in the SQLite database."""
    db: Session = SessionLocal()
    try:
        for hotel_name, dates in results.items():
            for date, data in dates.items():
                for provider, price in data.get("prices", {}).items():
                    db_result = TestResult(
                        hotel_name=hotel_name,
                        date=date,
                        provider=provider,
                        price=price,
                        screenshot=data.get("screenshot", "")
                    )
                    db.add(db_result)
        db.commit()
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
