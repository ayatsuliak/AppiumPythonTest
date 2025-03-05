from fastapi import FastAPI
from app.database import get_results, init_db
from app.redis_cache import get_cached_results

app = FastAPI()

init_db()

@app.get("/")
def home():
    return {"message": "API to get test results!"}

@app.get("/results")
def get_test_results():
    """Return all test results"""
    cached_results = get_cached_results()
    if cached_results:
        return {"source": "Redis", "results": cached_results}

    results = get_results()
    return {"source": "Database", "results": results}
