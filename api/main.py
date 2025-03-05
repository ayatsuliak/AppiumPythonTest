from fastapi import FastAPI
from app.database import get_results, init_db

app = FastAPI()

init_db()

@app.get("/")
def home():
    return {"message": "API to get test results!"}

@app.get("/results")
def get_test_results():
    """Return all test results"""
    results = get_results()
    return {"results": results}
