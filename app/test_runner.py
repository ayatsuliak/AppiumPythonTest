from appium import webdriver
import time
import json
from app.config import APPIUM_CAPS, APPIUM_SERVER

def run_test():
    driver = webdriver.Remote(APPIUM_SERVER, APPIUM_CAPS)
    time.sleep(5)  # Чекаємо запуск додатка

    # Тут буде логіка тесту (пошук готелю, отримання цін тощо)

    driver.quit()

    return {"status": "success", "message": "Test completed"}

if __name__ == "__main__":
    result = run_test()
    print(json.dumps(result, indent=4))
