# Appium Configuration
APPIUM_SERVER = "http://localhost:4723"
APPIUM_CAPS = {
    "platformName": "Android",
    "deviceName": "emulator-5554",
    "appPackage": "com.tripadvisor.tripadvisor",
    "appActivity": "com.tripadvisor.android.ui.launcher.LauncherActivity",
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
