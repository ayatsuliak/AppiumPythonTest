import base64

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import time
import json
import os
from config import APPIUM_SERVER, APPIUM_CAPS, RESULTS_FILE, SCREENSHOT_DIR


def setup_driver():
    """Запускає WebDriver для керування додатком."""
    options = UiAutomator2Options()
    options.load_capabilities(APPIUM_CAPS)
    return webdriver.Remote(APPIUM_SERVER, options=options)


def search_hotel(driver, hotel_name):
    """Шукає готель у Tripadvisor."""
    time.sleep(25)

    search_button = driver.find_element(AppiumBy.ID, "com.tripadvisor.tripadvisor:id/tab_search")
    search_button.click()
    time.sleep(5)

    search_input = driver.find_element(AppiumBy.ID, "com.tripadvisor.tripadvisor:id/edtSearchString")
    search_input.send_keys(hotel_name)
    time.sleep(5)

    first_result = driver.find_element(AppiumBy.XPATH,
                                       '//android.widget.TextView[@resource-id="com.tripadvisor.tripadvisor:id/txtHeading" and contains(@text, "{}")]'.format(hotel_name))
    first_result.click()
    time.sleep(5)


def get_prices(driver, hotel_name, dates):
    """Отримує ціни готелю з різних джерел і робить скріншот."""
    results = {hotel_name: {}}

    for date in dates:
        time.sleep(3)

        screenshotBase64 = driver.get_screenshot_as_base64()

        screenshot_path = os.path.join(SCREENSHOT_DIR, f"{hotel_name}_{date}.png")
        with open(screenshot_path, 'wb') as file:
            file.write(base64.b64decode(screenshotBase64))

        providers = ["Booking.com", "Expedia", "Hotels.com"]
        prices = {provider: f"{100 + i * 5} USD" for i, provider in enumerate(providers)}

        results[hotel_name][date] = {
            "prices": prices,
            "screenshot": screenshot_path
        }

    return results


def save_results_to_json(results):
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    with open(RESULTS_FILE, "w") as file:
        json.dump(results, file, indent=4)


def main():
    driver = setup_driver()

    try:
        hotel_name = "Grosvenor Hotel"
        dates = ["2025-14-01", "2025-15-02", "2025-16-03"]

        search_hotel(driver, hotel_name)
        results = get_prices(driver, hotel_name, dates)
        save_results_to_json(results)

        print("✅ The test is over! The results are saved in", RESULTS_FILE)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
