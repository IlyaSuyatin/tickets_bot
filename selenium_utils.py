import requests as rq
from datetime import date as dt
from selenium import webdriver as web
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

TICKETS_BASE_URL = "https://www.aviasales.com/search/"

def get_tickets (departure, origin, destination):
    driver = web.Chrome()
    driver.get(TICKETS_BASE_URL)
    time.sleep(1)
    consent_button = driver.find_element(By.CLASS_NAME, "fc-cta-consent")
    consent_button.click()
    time.sleep(0.5)
    origin_input = driver.find_element(By.ID, "avia_form_origin-input")
    origin_input.clear()
    time.sleep(0.5)
    origin_input.send_keys(origin)
    time.sleep(0.5)
    destination_input = driver.find_element(By.ID, "avia_form_destination-input")
    destination_input.send_keys(destination)
    time.sleep(0.5)
    departure_date = driver.find_element(By.CSS_SELECTOR, "[data-test-id=start-date-value]")
    departure_date.click()
    time.sleep(0.5)
    # date_button = driver.find_element(By.CSS_SELECTOR, f"[data-test-id=date-{departure}]")
    date_button = driver.find_element(By.CSS_SELECTOR, f'[data-test-id="date-{departure}"]')
    action = ActionChains(driver)
    action.move_to_element(date_button).perform()
    time.sleep(0.5)
    date_button.click()
    submit_button = driver.find_element(By.CSS_SELECTOR, "[data-test-id=form-submit]")
    submit_button.click()
    time.sleep(10)
    tickets = []
    ticket_containers = driver.find_elements(By.CSS_SELECTOR, '[data-test-id="ticket-preview"]')
    for ticket_container in ticket_containers:
        price = ticket_container.find_element(By.CSS_SELECTOR, "[data-test-id=price]").text
        origin_endpoint = ticket_container.find_element(By.CSS_SELECTOR, "[data-test-id=origin-endpoint]").text.replace("\u200a", "")
        destination_endpoint = ticket_container.find_element(By.CSS_SELECTOR, "[data-test-id=destination-endpoint]").text.replace("\u200a", "")
        tickets.append({
            "price":price,
            "origin_endpoint":origin_endpoint,
            "destination_endpoint":destination_endpoint
            })
    driver.quit()
    return(tickets)

