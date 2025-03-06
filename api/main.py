import uvicorn

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.redis_cache import get_cached_results
from app.database import get_db, TestResult

app = FastAPI()

get_db()

@app.get("/")
def home():
    return {"message": "API to get test results!"}

@app.get("/results")
def get_test_results(db: Session = Depends(get_db)):
    """Return all test results"""
    cached_results = get_cached_results()
    if cached_results:
        return {"source": "Redis", "results": cached_results}

    db_results = db.query(TestResult).all()
    results = {}
    for result in db_results:
        if result.hotel_name not in results:
            results[result.hotel_name] = {}
        results[result.hotel_name][result.date] = {
            "provider": result.provider,
            "price": result.price,
            "screenshot": result.screenshot
        }

    return {"source": "Database", "results": results}

if __name__ == '__main__':
    get_db()
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)
