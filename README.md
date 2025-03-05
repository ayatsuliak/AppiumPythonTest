# 📌 Test Automation with Appium, FastAPI & Redis

## **Project Overview**
This project automates hotel price retrieval from the **Tripadvisor app** using **Appium** and stores the results in **SQLite** and **Redis** for caching. Additionally, it provides a **FastAPI-based REST API** to access the test results.

---

## **📂 Project Structure**
```
AppiumPythonTest/
|── api/
│   ├── __init__.py
│   ├── main.py               # API server (FastAPI)
│── app/
│   ├── __init__.
│   ├── appium_helpers.py     # Appium WebDriver setup and utilities
│   ├── database.py           # SQLite database functions
│   ├── redis_cache.py        # Redis caching functions
│   ├── test_runner.py        # Runs the Appium tests
│── config.py                 # Configuration settings
│── README.md                 # Instructions
│── requirements.txt          # Dependencies
│── results.db                # SQLite database file
│── results.json              # Sample test results
```

---

## **1️⃣ Configuration (`config.py`)**
Before running the project, ensure that your **configuration settings** are correct.

📜 **Modify `config.py` if necessary:**

```python
# Appium Configuration
APPIUM_SERVER = "http://localhost:4723/wd/hub"
APPIUM_CAPS = {
    "platformName": "Android",
    "deviceName": "emulator-5554",
    "appPackage": "com.tripadvisor.tripadvisor",
    "appActivity": "com.tripadvisor.android.activity.LaunchActivity",
    "automationName": "UiAutomator2",
    "noReset": True
}

# Redis Configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# SQLite Database
DB_FILE = "results.db"

# File Paths
RESULTS_FILE = "results.json"
SCREENSHOT_DIR = "app/screenshots/"
```

---

## **2️⃣ Install Dependencies**
Ensure you have Python **3.8+** installed.

### **🔹 Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate     # Windows
```

### **🔹 Install all required Python packages**
```bash
pip install -r requirements.txt
```

---

## **3️⃣ Setup Redis & SQLite**
### **🔹 Start Redis server**
```bash
redis-server
```
### **🔹 Verify Redis is running**
```bash
redis-cli ping
# Response: PONG
```
### **🔹 Initialize the SQLite database**
```bash
python -c "from app.database import init_db; init_db()"
```

---

## **4️⃣ Run the API Server (`api/main.py`)**
Start the **FastAPI** server to access test results.
```bash
uvicorn api.main:app --reload
```
### **🔹 API Endpoints:**
| Method | Endpoint       | Description                 |
|--------|---------------|-----------------------------|
| GET    | `/`           | API status check           |
| GET    | `/results`    | Retrieve test results      |

📌 **Visit Swagger UI for API testing:**
👉 `http://127.0.0.1:8000/docs`

---

## **5️⃣ Run the Appium Server**
Open **Command Prompt** and start the **Appium** Server.
```bash
appium
```

---

## **6️⃣ Run Automated Tests (`app/test_runner.py`)**
This script launches the **Tripadvisor app**, selects a hotel, picks dates, fetches prices, and stores results in **Redis & SQLite**.
```bash
python -m app.test_runner
```
✅ After execution, results will be available in:
- **Redis (cached for 1 hour)**
- **SQLite (`results.db`)**
- **API (`GET /results`)**

---


## **❌Common Issues & Fixes**
| Issue | Solution                                                                |
|-------|-------------------------------------------------------------------------|
| Appium server not running | Start Appium manually: `appium --allow-cors`                               |
| Redis connection error | Ensure Redis is running: `redis-server`                                 |
| Database issues | Reinitialize: `python -c "from app.database import init_db; init_db()"` |
| No test results found | Run tests again: `python app/test_runner.py`                            |

---

## **📌 Summary**
✅ **Automates hotel price retrieval with Appium**  
✅ **Stores results in SQLite & Redis for caching**  
✅ **Provides a REST API to access test data**  
✅ **Uses FastAPI, Redis & Appium WebDriver**  

🚀 **Now you're ready to run automated tests & fetch results via API!**
