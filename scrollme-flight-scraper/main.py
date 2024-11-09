from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager
import time
from datetime import datetime, timedelta
from threading import Thread
import pandas as pd
import pygame
import re
import os

## Set up headless options for Firefox
service = Service(GeckoDriverManager().install())
options = webdriver.FirefoxOptions()
options.headless = True

# Initialize the browser
url = "https://www.google.com/travel/flights?gl=IN&hl=en"
browser = webdriver.Firefox(service=service, options=options)
browser.get(url)
browser.maximize_window()
wait = WebDriverWait(browser, 10)
pygame.mixer.init()
success_sound = "success.mp3"
error_sound = "error.mp3"


def play_sound(sound_type="success"):
    # Load the corresponding file based on sound_type
    if sound_type == "success":
        pygame.mixer.music.load(success_sound)
    elif sound_type == "error":
        pygame.mixer.music.load(error_sound)

    pygame.mixer.music.play()

    # Optional: Wait until the sound finishes playing
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)


# Non-blocking play sound function
def play_sound_non_blocking(sound_type="success"):
    Thread(target=play_sound, args=(sound_type,)).start()


# Define city pairs and date range
origins = [
    "Kolkata",
]
destinations = ["Delhi", "Mumbai", "Chennai", "Bengaluru", "Hyderabad"]
start_date = datetime(2024, 12, 10)  # Starting from Sat, Nov 10
end_date = datetime(2025, 2, 28)

# Generate dates in the required format
date_list = [
    (start_date + timedelta(days=x)).strftime("%a, %b %d")
    for x in range((end_date - start_date).days + 1)
]


# Utility function for safe element retrieval
def safe_find_element(element, by, path):
    try:
        return element.find_element(by, path).text
    except NoSuchElementException:
        return "NA"


def save_to_csv(data, filename):
    # If the file is already exists, append without the header
    if os.path.isfile(filename):
        data.to_csv(filename, mode="a", header=False, index=False, encoding="utf-8")
    else:
        data.to_csv(filename, mode="w", header=True, index=False, encoding="utf-8")


# Collect data
flights_data = []

for origin in origins:
    for destination in destinations:
        for target_date in date_list:
            # Local current_flight_data = []
            current_flight_data = []
            try:
                # Locate and interact with the "from" input field
                from_input = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input",
                        )
                    )
                )
                from_input.clear()
                from_input.send_keys(origin)

                # Wait for the suggestion to be clickable and then click it
                from_input_option = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[3]/ul/li[1]/div[2]",
                        )
                    )
                )
                from_input_option.click()

                # Locate and interact with the "to" input field
                to_input = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[4]/div/div/div[1]/div/div/input",
                        )
                    )
                )
                to_input.clear()
                to_input.send_keys(destination)

                # Wait for the suggestion to be clickable and then click it
                to_input_option = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[3]/ul/li[1]/div[2]",
                        )
                    )
                )
                to_input_option.click()

                # Locate and interact with the "departure input field
                departure_input = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input",
                        )
                    )
                )

                departure_input.clear()
                departure_input.send_keys(target_date)
                departure_input.send_keys(Keys.TAB)
                time.sleep(1)

                # Locate and interact with the "return input field
                return_input = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[2]/div/input",
                        )
                    )
                )
                return_input.clear()
                return_input.send_keys(target_date)
                return_input.send_keys(Keys.TAB)
                time.sleep(1)
                try:
                    done_button = wait.until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[3]/div[3]/div/button",
                            )
                        )
                    )
                    browser.execute_script(
                        "arguments[0].scrollIntoView();", done_button
                    )
                    browser.execute_script("arguments[0].click();", done_button)
                    time.sleep(2)
                except TimeoutException:
                    print("done button not found!")

                explore_button = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button",
                        )
                    )
                )
                browser.execute_script("arguments[0].scrollIntoView();", explore_button)
                browser.execute_script("arguments[0].click();", explore_button)
                # explore_button.click()
                time.sleep(2)

                # Expand flights data button
                try:
                    time.sleep(2)
                    # Scroll down 300 pixels
                    browser.execute_script("window.scrollBy(0, 800);")
                    try:
                        expand_flight_data_button = wait.until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[2]/div/div[2]/div[4]/ul/li[*]/div/span[1]/div/button",
                                )
                            )
                        )
                        browser.execute_script(
                            "arguments[0].scrollIntoView();", expand_flight_data_button
                        )
                        browser.execute_script(
                            "arguments[0].click();", expand_flight_data_button
                        )
                        # expand_flight_data_button.click()
                        time.sleep(5)
                        # Locate all the li elements with 'pIav2d' class name
                        flights_elements = wait.until(
                            EC.presence_of_all_elements_located(
                                (By.CLASS_NAME, "pIav2d")
                            )
                        )

                        print(f"Locate all the li elements with 'pIav2d' class! ")

                        # Iterate through each flights element and extract the data
                        for flight in flights_elements:
                            try:
                                airline = safe_find_element(
                                    flight,
                                    By.CSS_SELECTOR,
                                    "div > div.yR1fYc > div > div.OgQvJf.nKlB3b > div > div.Ir0Voe > div.sSHqwe.tPgKwe.ogfYpf > span:nth-child(1)",
                                )
                                flight_arrival_time = safe_find_element(
                                    flight,
                                    By.CSS_SELECTOR,
                                    "div > div.yR1fYc > div > div.OgQvJf.nKlB3b > div > div.Ir0Voe > div.zxVSec.YMlIz.tPgKwe.ogfYpf > span > span:nth-child(1) > span > span > span",
                                )
                                flight_departure_time = safe_find_element(
                                    flight,
                                    By.CSS_SELECTOR,
                                    "div > div.yR1fYc > div > div.OgQvJf.nKlB3b > div > div.Ir0Voe > div.zxVSec.YMlIz.tPgKwe.ogfYpf > span > span:nth-child(2) > span > span > span",
                                )
                                flight_duration = safe_find_element(
                                    flight,
                                    By.CSS_SELECTOR,
                                    "div > div.yR1fYc > div > div.OgQvJf.nKlB3b > div > div.Ak5kof > div",
                                )
                                flights_stops = safe_find_element(
                                    flight,
                                    By.CSS_SELECTOR,
                                    "div > div.yR1fYc > div > div.OgQvJf.nKlB3b > div > div.BbR8Ec > div.EfT7Ae.AdWm1c.tPgKwe > span",
                                )
                                carbon_emission = safe_find_element(
                                    flight,
                                    By.CSS_SELECTOR,
                                    "div > div.yR1fYc > div > div.OgQvJf.nKlB3b > div > div.y0NSEe.V1iAHe.tPgKwe.ogfYpf > div > div.O7CXue > div",
                                )
                                flight_price = safe_find_element(
                                    flight,
                                    By.CSS_SELECTOR,
                                    "div > div.yR1fYc > div > div.OgQvJf.nKlB3b > div > div.U3gSDe > div.BVAVmf.I11szd.POX3ye > div.YMlIz.FpEdX > span",
                                )

                                # # Click on expand icon
                                more_info_button = flight.find_element(
                                    By.CSS_SELECTOR,
                                    "div > div:nth-child(3) > div > div > button",
                                )
                                browser.execute_script(
                                    "arguments[0].scrollIntoView();", more_info_button
                                )
                                time.sleep(1)
                                # more_info_button.click()
                                browser.execute_script(
                                    "arguments[0].click();", more_info_button
                                )
                                time.sleep(1)

                                # Additional Information
                                flight_number = flight.find_element(
                                    By.CSS_SELECTOR,
                                    "div > div.m9ravf > div > div.c257Jb.QwxBBf.eWArhb > div.MX5RWe.sSHqwe.y52p7d > span.Xsgmwe.QS0io",
                                ).text
                                aircraft_company = flight.find_element(
                                    By.CSS_SELECTOR,
                                    "div > div.m9ravf > div > div.c257Jb.QwxBBf.eWArhb > div.MX5RWe.sSHqwe.y52p7d > span:nth-child(8)",
                                ).text
                                date = flight.find_element(
                                    By.CSS_SELECTOR,
                                    "div > div.yR1fYc > div > div.fBultf.kvnVYc.Q7Ypyb > div.rarCGf > div.S90skc.y52p7d.ogfYpf > span:nth-child(3)",
                                ).text

                                filename = f"{origin}_{
                                    destination}_flight_data.csv"
                                # Only extract and convert to integer if flight_price contains a valid number
                                flight_price_value = (
                                    int(re.sub(r"[^\d]", "", flight_price))
                                    if re.search(r"\d", flight_price)
                                    else None
                                )

                                # Append data to the list
                                current_flight = {
                                    "Airline": airline,
                                    "Flight Number": flight_number,
                                    "Aircraft Company": aircraft_company,
                                    "Origin": origin,
                                    "Destination": destination,
                                    "Arrival Time": flight_arrival_time,
                                    "Departure Time": flight_departure_time,
                                    "Flight Duration": flight_duration,
                                    "Flight Stops": flights_stops,
                                    "Carbon Emission": carbon_emission,
                                    "Flight Price": flight_price_value,
                                    "Date": date,
                                }
                                if (
                                    airline
                                    and flight_arrival_time
                                    and flight_departure_time
                                    and flight_price_value
                                ):
                                    flights_data.append(current_flight)
                                    current_flight_data.append(current_flight)
                                    print(f"flight ${current_flight}")
                                    play_sound_non_blocking("success")
                                else:
                                    print(
                                        "Incomplete flight data encountered; skipping this entry."
                                    )
                                    play_sound_non_blocking("error")
                                    browser.get(url)
                                    time.sleep(10)
                                    break

                            except (TimeoutException, NoSuchElementException) as e:
                                print(
                                    f"Error: {e} for route {origin} to {
                                        destination} on {target_date}"
                                )
                                play_sound_non_blocking("error")
                        df = pd.DataFrame(current_flight_data)
                        save_to_csv(df, "scrollme_flights_data.csv")
                        filename_df = pd.DataFrame(current_flight_data)
                        save_to_csv(filename_df, filename)
                        print("Flight data has been saved to scrollme_flights_data.csv")
                        browser.get(url)
                        print("browser back to home page...")
                        play_sound_non_blocking("success")
                        time.sleep(10)
                    except TimeoutException:
                        print("Expand button not available!")
                        browser.get(url)
                        time.sleep(10)
                        continue

                except TimeoutException:
                    airline = wait.until(
                        EC.presence_of_element_located(
                            By.XPATH,
                            '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[2]/div/div[2]/div[3]/ul/li[1]/div/div[2]/div/div[2]/div/div[2]/div[2]/span',
                        )
                    )
                    print(f"Airline {airline}")
                    print(
                        "Expand flights data button not found; proceeding without clicking."
                    )
                    play_sound_non_blocking("error")

            except (TimeoutException, NoSuchElementException) as e:
                print(
                    f"Error: {e} for route {origin} to {
                        destination} on {target_date}"
                )
            finally:
                # Save data after each iteration
                flight_data_df = pd.DataFrame(flights_data)
                save_to_csv(flight_data_df, "flights_data.csv")
                play_sound_non_blocking("success")


time.sleep(10)
# Close the browser after the loop completes
browser.quit()
print("Data collection complete and saved to flights_data.csv")
