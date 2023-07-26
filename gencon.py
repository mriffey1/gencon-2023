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
select_query = "SELECT url, last_msg, event_time, isPastEvent FROM gencon WHERE isPastEvent = 0"
cursor.execute(select_query)
rows = cursor.fetchall()

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
counter = 0

for row in rows:
    url = row[0]
    last_msg_time = row[1] # Last msg time retrieved from the database
    event_time_db = row[2] 
    isPastEventDB = row[3]
    
    
# Checks event time. If 5 minutes or less to the event, it gets marked as a 1 to be excluded moving forward.
    if (event_time_db - datetime.datetime.now()).total_seconds() <= 300:
        update_query = "UPDATE events SET isPastEvent = %s WHERE url = %s"
        cursor.execute(update_query, (1, url))
        db_connection.commit()
    else:
            driver.get(url)
            time.sleep(0.10)
            
            WebDriverWait(driver, 0.10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'page-title')]",)))
            
            title_event = driver.find_element(By.XPATH, ".//div[contains(@class, 'page-title')]").text
            
            available_tickets = driver.find_element(By.XPATH,".//div[contains(@id, 'event_detail_ticket_purchase')]//following::p[1]",).text
            
            event_datetime = driver.find_element(By.XPATH,".//a[contains(@title, 'Find other events on this day')]",).text

            event_date = event_datetime.replace(",", "").strip()

            formatted_ticket_amount = int(available_tickets.replace("Available Tickets: ", "").strip())
            
            if formatted_ticket_amount > 0:
                has_ticket = True
                print("IT'S GOT TICKETS")
                
                if (last_msg_time is None or (datetime.datetime.now() - last_msg_time).total_seconds() >= 900 and isPastEventDB == 0):
                    subject_msg = (str(formatted_ticket_amount) + " available: " + title_event.title())
                    type_email = "tickets"
                    text_notification.send_email(str(event_date), title_event.title(), str(formatted_ticket_amount), url, type_email)
                    counter += 1
                    
                    # Update the last msg time in the database
                    update_query = "UPDATE gencon SET last_msg = %s WHERE url = %s"
                    cursor.execute(update_query, (datetime.datetime.now(), url))
                    db_connection.commit()
            else:
               counter = 0

if counter == 0:
    print("No events have tickets")
else:
    print("A event has tickets")

now = datetime.datetime.today()
dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
print("Script ended at " + dt_string + ".")
print("------------------------------")
cursor.close()
db_connection.close()
driver.quit()
