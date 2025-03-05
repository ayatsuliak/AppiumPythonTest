import base64
import os
import time
import json
from datetime import timedelta
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import APPIUM_SERVER, APPIUM_CAPS, SCREENSHOT_DIR, RESULTS_FILE


def setup_driver():
    """Initializes Appium WebDriver."""
    options = UiAutomator2Options()
    options.load_capabilities(APPIUM_CAPS)
    return webdriver.Remote(APPIUM_SERVER, options=options)


def search_hotel(driver, hotel_name):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "com.tripadvisor.tripadvisor:id/tab_search"))).click()

    search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "com.tripadvisor.tripadvisor:id/edtSearchString")))
    search_input.send_keys(hotel_name)

    first_result = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//android.widget.TextView[@resource-id="com.tripadvisor.tripadvisor:id/txtHeading" and contains(@text, "{hotel_name}")]'))
    )
    first_result.click()
    time.sleep(3)


def select_dates(driver, check_in_date):
    try:
        date_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//android.view.ViewGroup[@resource-id='com.tripadvisor.tripadvisor:id/hotelInfoInputField']"))
        )
        date_field.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@resource-id='com.tripadvisor.tripadvisor:id/monthView']"))
        )

        while True:
            try:
                driver.find_element(By.XPATH,
                                    f"//android.widget.TextView[@resource-id='com.tripadvisor.tripadvisor:id/txtTitle' and contains(@text, '{check_in_date.strftime('%B')}')]")
                break
            except:
                next_month_button = driver.find_element(By.XPATH, "//android.widget.Button[contains(@resource-id, 'btnNext')]")
                next_month_button.click()
                time.sleep(1)

        check_in_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        f"//android.widget.TextView[@resource-id='com.tripadvisor.tripadvisor:id/txtDay' and @text='{check_in_date.day}']"))
        )
        check_in_element.click()

        check_out_date = check_in_date + timedelta(days=1)
        check_out_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        f"//android.widget.TextView[@resource-id='com.tripadvisor.tripadvisor:id/txtDay' and @text='{check_out_date.day}']"))
        )
        check_out_element.click()

        apply_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//android.widget.Button[@resource-id='com.tripadvisor.tripadvisor:id/btnPrimary']"))
        )
        apply_button.click()
        time.sleep(10)

    except Exception as e:
        print(f"❌ Error when selecting a date: {e}")


def get_prices(driver, hotel_name, check_in_date):
    screenshot_path = os.path.join("app/screenshots/", f"{hotel_name}_{check_in_date.strftime('%Y-%m-%d')}.png")

    screenshotBase64 = driver.get_screenshot_as_base64()
    with open(screenshot_path, 'wb') as file:
        file.write(base64.b64decode(screenshotBase64))

    prices = {}

    try:
        providers = driver.find_elements(By.XPATH, "//android.widget.ImageView[@resource-id='com.tripadvisor.tripadvisor:id/imgProviderLogo']")

        prices_elements = driver.find_elements(By.XPATH,
                                               "//android.widget.TextView[@resource-id='com.tripadvisor.tripadvisor:id/txtPrice']")

        if not providers or not prices_elements:
            print("⚠ No providers or prices found!")

        for provider, price in zip(providers, prices_elements):
            provider_name = provider.get_attribute("content-desc").strip()

            if not provider_name:
                provider_name = "Unknown Provider"

            price_value = price.text.strip()
            prices[provider_name] = price_value

    except Exception as e:
        print(f"❌ Unable to get prices: {e}")

    return {
        "prices": prices,
        "screenshot": screenshot_path
    }


def save_results_to_json(results):
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    with open(RESULTS_FILE, "w") as file:
        json.dump(results, file, indent=4)
