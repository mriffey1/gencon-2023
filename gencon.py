from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import text_msg as text_notification
import time
import pickle
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime as datetime

now = datetime.datetime.today()
dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
print("Script started at " + dt_string + "\n")
print("------------------------------")
s = Service(executable_path="/usr/lib/chromium-browser/chromedriver")


def chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
    )
    options.add_argument("--headless=new")
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

data = {
    "events": [
        "https://www.gencon.com/events/232688",
        "https://www.gencon.com/events/235160",
        "https://www.gencon.com/events/233584",
        "https://www.gencon.com/events/235161",
        "https://www.gencon.com/events/221288",
        "https://www.gencon.com/events/231853",
        "https://www.gencon.com/events/231851",
        "https://www.gencon.com/events/221289",
        "https://www.gencon.com/events/231852",
        "https://www.gencon.com/events/235158",
        "https://www.gencon.com/events/220692",
    ],
    "hosts": ["https://www.gencon.com/event_finder?host=Steamforged+Games&c=indy2023"],
}

driver = webdriver.Chrome(service=s, options=options)

driver.get("https://www.gencon.com/login")

cookies = pickle.load(open("/home/megan/Documents/Python/gencon/cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

time.sleep(2)
driver.refresh()
has_ticket = False
for key, value in data.items():
    if key == "events":
        for event_url in value:
            driver.get(event_url)
            time.sleep(3)
            WebDriverWait(driver, 2).until(
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
                subject_msg = (
                    str(formatted_ticket_amount) + " available: " + title_event.title()
                )
                type_email = "tickets"
                text_notification.send_email(
                    str(event_date),
                    title_event.title(),
                    str(formatted_ticket_amount),
                    event_url,
                    type_email,
                )
            else:
                print(title_event.title() + " has no tickets")
    # elif key == "lorcana":
    #     for event_url in value:
    #         driver.get(event_url)
    #         time.sleep(3)
    #         WebDriverWait(driver, 2).until(
    #             EC.presence_of_element_located(
    #                 (
    #                     By.XPATH,
    #                     "//div[contains(@class, 'page-title')]",
    #                 )
    #             )
    #         )
    #         title_event = driver.find_element(
    #             By.XPATH, ".//div[contains(@class, 'page-title')]"
    #         ).text
    #         available_tickets = driver.find_element(
    #             By.XPATH,
    #             ".//div[contains(@id, 'event_detail_ticket_purchase')]//following::p[1]",
    #         ).text
    #         event_datetime = driver.find_element(
    #             By.XPATH,
    #             ".//a[contains(@title, 'Find other events on this day')]",
    #         ).text

    #         event_date = event_datetime.replace(",", "").strip()

    #         formatted_ticket_amount = int(
    #             available_tickets.replace("Available Tickets: ", "").strip()
    #         )
    #         if formatted_ticket_amount > 0:
    #             has_ticket = True
    #             print("IT'S GOT TICKETS")
    #             subject_msg = (
    #                 str(formatted_ticket_amount) + " available: " + title_event.title()
    #             )
    #             type_email = "tickets"
    #             text_notification.send_email(
    #                 str(event_date),
    #                 title_event.title(),
    #                 str(formatted_ticket_amount),
    #                 event_url,
    #                 type_email,
    #             )
    elif key == "hosts":
        for host_url in value:
            driver.get(host_url)
            host_events = driver.find_element(
                By.XPATH, '//*[@id="page"]/div[2]/div/div/div/div/div[2]/div[1]/p'
            ).text
            formatted_event_amount = int(
                host_events.replace("Found ", "").replace(" events", "").strip()
            )
            if formatted_event_amount > 0:
                print("Steamforged Added Events")
                subject_msg = "Steamforged has added events"
                type_email = "events"
                text_notification.send_email(
                    subject_msg,
                    "Steamforged Games",
                    str(formatted_event_amount),
                    host_url,
                    type_email,
                )
            print("No Steamforged Events")

    else:
        print("Unknown key:", key)

now = datetime.datetime.today()
dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
print("Script ended at " + dt_string + "\n")
print("------------------------------")
driver.quit()
