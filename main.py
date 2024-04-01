import requests as rq
import bs4
import os
from datetime import date as dt
from selenium import webdriver as web
from selenium.webdriver.common.by import By
import time

TICKETS_BASE_URL = "https://www.aviasales.com/search/"
CODES_URL = "https://www.bts.gov/topics/airlines-and-airports/world-airport-codes"
FILE = "codes.txt"

codes = []

if not os.path.exists(FILE):
    responce = rq.get(CODES_URL)
    soup = bs4.BeautifulSoup(responce.content, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")

    for raw in rows[1:]:
        columns = raw.find_all("td")
        code = columns[0].text
        city = columns[1].text
        with open(FILE, "a") as file:
            file.write(f"{code}|{city}\n")

with open(FILE)as file:
    rows = file.readlines()
    for row in rows:
        columns = row.split("|")
        code = columns[0]
        city = columns[1]
        codes.append({
            "code": code, "city": city
        })

    
city_from = "Skelleftea"
city_to = "Stockholm"
city_from_airports = []
city_to_airports = []
city_from_airport = None
city_to_airport = None
departure_date = None
return_date = None

for airport in codes:
    if city_from in airport["city"]:
        city_from_airports.append(airport)
    if city_to in airport["city"]:
        city_to_airports.append(airport)


if len(city_from_airports) > 0:
    if len(city_from_airports) > 1:
        for variant in city_from_airports:
            print(variant)
        city_from_airport = city_from_airports[int(input())]
    else:
        city_from_airport = city_from_airports[0]
else:
    print("not found")


if len(city_to_airports) > 0:
    if len(city_to_airports) > 1:
        for variant in city_to_airports:
            print(variant)
        city_to_airport = city_to_airports[int(input())]
    else:
        city_to_airport = city_to_airports[0]
else:
    print("not found")
print(city_from_airport, city_to_airport)

return_ticket = True

while True:
    print("do you want a return ticket? (yes/no)")
    ticket_answer = input().lower()

    if ticket_answer == "yes":
        break
    elif ticket_answer == "no":
        return_ticket = False
        break
    else:
        print("error, try again")
# print(return_ticket)

departure_date = dt(2024, 4, 29)
return_date = dt(2024, 5, 2)
return_date_month = return_date.month
return_date_day = return_date.day
departure_date_month = departure_date.month
departure_date_day = departure_date.day

def dateSolver (raw_data):
    if raw_data <= 9:
        raw_data = "0" + str(raw_data)
    return(raw_data)

return_date_month = dateSolver(return_date_month)
return_date_day = dateSolver(return_date_day)
departure_date_month = dateSolver(departure_date_month)
departure_date_day = dateSolver(departure_date_day)

if return_ticket == False:
    return_date_month = ""
    return_date_day = ""

url = f"{TICKETS_BASE_URL}{city_from_airport['code']}{departure_date_day}{departure_date_month}{city_to_airport['code']}{return_date_day}{return_date_month}1"

# responce = rq.get(url)
print(url)
# soup = bs4.BeautifulSoup(responce.content, "html.parser")
# search_results = soup.find_all("div", attrs={"class":"app__content"})
# print(search_results)


driver = web.Chrome()
driver.get(url)
time.sleep(5)
search_results = driver.find_elements(By.CSS_SELECTOR, ".s__KLpakf2_t1vV8fx1QJMO.s__nyn2SIjtBBP4lkYrqM1A.s__Z_M86eYiGhMPCOMX0AOT.s__vizY3leqG6q7isw6LLEc")
for result in search_results:
    print(result.text)
input()

