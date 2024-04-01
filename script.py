import requests as rq
from datetime import date as dt
from selenium import webdriver as web
from selenium.webdriver.common.by import By
import time

TICKETS_BASE_URL = "https://www.aviasales.com/search/"
departure = "11.04.2024"
driver = web.Chrome()
driver.get(TICKETS_BASE_URL)
time.sleep(3)
consent_button = driver.find_element(By.CLASS_NAME, "fc-cta-consent")
consent_button.click()
time.sleep(1)
origin_input = driver.find_element(By.ID, "avia_form_origin-input")
origin_input.clear()
time.sleep(1)
origin_input.send_keys("Skelleftea")
time.sleep(1)
destination_input = driver.find_element(By.ID, "avia_form_destination-input")
destination_input.send_keys("Stockholm")
time.sleep(1)
departure_date = driver.find_element(By.CSS_SELECTOR, "[data-test-id=start-date-value]")
departure_date.click()
time.sleep(2)
# date_button = driver.find_element(By.CSS_SELECTOR, f"[data-test-id=date-{departure}]")
date_button = driver.find_element(By.CSS_SELECTOR, '[data-test-id="date-11.04.2024"]')
date_button.click()
submit_button = driver.find_element(By.CSS_SELECTOR, "[data-test-id=form-submit]")
submit_button.click()

input()


