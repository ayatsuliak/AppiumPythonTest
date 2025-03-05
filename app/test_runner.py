from datetime import datetime
from appium_helpers import setup_driver, search_hotel, select_dates, get_prices, save_results_to_json
from config import RESULTS_FILE
from database import save_results
from redis_cache import cache_results


def main():
    driver = setup_driver()

    try:
        hotel_name = "Grosvenor Hotel"
        dates = [datetime(2025, 3, 14), datetime(2025, 3, 16),
                 datetime(2025, 3, 19), datetime(2025, 3, 22),
                 datetime(2025, 3, 29)]

        search_hotel(driver, hotel_name)

        results = {}
        for check_in_date in dates:
            select_dates(driver, check_in_date)
            results[check_in_date.strftime("%Y-%m-%d")] = get_prices(driver, hotel_name, check_in_date)

        cache_results(results)
        save_results(results, hotel_name)
        save_results_to_json(results)

        print("✅ The test is over! The results are saved in", RESULTS_FILE)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
