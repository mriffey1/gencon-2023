from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import text_msg as text_notification
import time
import pickle
import datetime as datetime
import utils
from utils import connect_to_database

db_connection, cursor = connect_to_database()
rows = utils.fetch_events_to_update(cursor)

now = datetime.datetime.today()
dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
print("Script started at " + dt_string)

s = Service(executable_path="/usr/lib/chromium-browser/chromedriver")
options = utils.chrome_options()
driver = webdriver.Chrome(service=s, options=options)

driver.get("https://www.gencon.com/login")

cookies = pickle.load(open("/home/megan/Documents/Python/gencon/cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
driver.refresh()

has_ticket = False

for row in rows:
    url, last_msg_time, event_time_db, isPastEventDB, title_event = row

# Checks event time. If 5 minutes or less to the event, it gets marked as a 1 to be excluded moving forward.
    if (event_time_db - datetime.datetime.now()).total_seconds() <= 300:
        utils.update_event_status(cursor, db_connection, url, 1)
    else:
            driver.get(url)
            
            WebDriverWait(driver, 0.05).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'page-title')]",)))
            
            available_tickets = driver.find_element(By.XPATH,".//div[contains(@id, 'event_detail_ticket_purchase')]//following::p[1]",).text
            
            event_date = event_time_db.strftime("%A %-I:%M %p EDT")

            formatted_ticket_amount = int(available_tickets.replace("Available Tickets: ", "").strip())
            
            if formatted_ticket_amount >= 2:
                has_ticket = True
                
                if (last_msg_time is None or (datetime.datetime.now() - last_msg_time).total_seconds() >= 900):
                    
                    subject_msg = (str(formatted_ticket_amount) + " available: " + title_event.title())
                    type_email = "tickets"
                    text_notification.send_email(str(event_date), title_event.title(), str(formatted_ticket_amount), url, type_email)
                    
                    print(subject_msg)
                    
                    # Update the last msg time in the database
                    utils.update_last_msg_time(cursor, db_connection, url)

now = datetime.datetime.today()
dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
print("Script ended at " + dt_string + ".")
print("------------------------------")

cursor.close()
db_connection.close()
driver.quit()
