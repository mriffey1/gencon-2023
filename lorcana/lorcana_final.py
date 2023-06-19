from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import tweet_msg as text_notification
import pickle
import datetime as datetime
import mysql.connector
from utils import utils_lorcana


dbhost, dbusername, dbpassword, dbname = utils_lorcana.database_stuff()

now = datetime.datetime.today()
dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
print("Lorcana started at " + dt_string + "")

s = Service(executable_path="/usr/lib/chromium-browser/chromedriver")


def chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
    )
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-gpu")  ##renderer timeout
    options.add_argument("--start-maximized")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--enable-javascript")

    return options


options = chrome_options()

driver = webdriver.Chrome(service=s, options=options)

driver.get("https://www.gencon.com/login")

cookies = pickle.load(open("/home/megan/Documents/Python/gencon/cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()
has_ticket = False

# Establish a connection to the MariaDB database


# Create a cursor to execute SQL queries


# Query the URLs and last tweet times from the "events" table
select_query = "SELECT url, last_tweet FROM events"
cursor.execute(select_query)
rows = cursor.fetchall()

for row in rows:
    url = row[0]
    last_tweet_time = row[1]  # Last tweet time retrieved from the database

    driver.get(url)
    WebDriverWait(driver, 0.10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//div[contains(@class, 'page-title')]",
            )
        )
    )
    title_event = driver.find_element(
        By.XPATH, ".//div[contains(@class, 'page-title')]"
    ).text
    available_tickets = driver.find_element(
        By.XPATH,
        ".//div[contains(@id, 'event_detail_ticket_purchase')]//following::p[1]",
    ).text
    event_datetime = driver.find_element(
        By.XPATH,
        ".//a[contains(@title, 'Find other events on this day')]",
    ).text

    event_date = event_datetime.replace(",", "").strip()

    formatted_ticket_amount = int(
        available_tickets.replace("Available Tickets: ", "").strip()
    )
    if formatted_ticket_amount > 0:
        has_ticket = True
        print("IT'S GOT TICKETS")
        if (
            last_tweet_time is None
            or (datetime.datetime.now() - last_tweet_time).total_seconds() >= 900
        ):
            # Enough time has passed, send a tweet
            tweet_message = (
                str(formatted_ticket_amount) + " available: " + title_event.title()
            )
            print(tweet_message)
            type_email = "tickets"
            text_notification.send_email(
                str(event_date),
                title_event.title(),
                str(formatted_ticket_amount),
                url,
                type_email,
            )

            # Update the last tweet time in the database
            update_query = "UPDATE events SET last_tweet = %s WHERE url = %s"
            cursor.execute(update_query, (datetime.datetime.now(), url))
            db_connection.commit()

now = datetime.datetime.today()
dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
print("Script ended at " + dt_string + "")
print("------------------------------")

# Close the cursor and database connection
cursor.close()
db_connection.close()
driver.quit()
