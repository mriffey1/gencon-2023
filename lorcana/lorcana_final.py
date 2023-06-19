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
import utils_lorcana

dbhost, dbusername, dbpassword, dbname = utils_lorcana.database_stuff()

now = datetime.datetime.today()
dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
print("Lorcana started at " + dt_string + "")

s = Service(executable_path="/usr/lib/chromium-browser/chromedriver")

options = utils_lorcana.chrome_options()

driver = webdriver.Chrome(service=s, options=options)

driver.get("https://www.gencon.com/login")

cookies = pickle.load(open("/home/megan/Documents/Python/gencon/cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()
has_ticket = False

db_connection = mysql.connector.connect(host=dbhost, user=dbusername, password=dbpassword, database=dbname)

cursor = db_connection.cursor()

select_query = "SELECT url, last_tweet FROM events"
cursor.execute(select_query)
rows = cursor.fetchall()

for row in rows:
    url = row[0]
    last_tweet_time = row[1]  # Last tweet time retrieved from the database

    driver.get(url)
    WebDriverWait(driver, 0.10).until(EC.presence_of_element_located((By.XPATH,"//div[contains(@class, 'page-title')]",)))
    
    title_event = driver.find_element(By.XPATH, ".//div[contains(@class, 'page-title')]").text
    
    available_tickets = driver.find_element(By.XPATH,".//div[contains(@id, 'event_detail_ticket_purchase')]//following::p[1]",).text
    
    event_datetime = driver.find_element(By.XPATH,".//a[contains(@title, 'Find other events on this day')]",).text

    event_date = event_datetime.replace(",", "").strip()

    formatted_ticket_amount = int(available_tickets.replace("Available Tickets: ", "").strip())
    
    if formatted_ticket_amount > 0:
        has_ticket = True
        print("IT'S GOT TICKETS")
        if (last_tweet_time is None or (datetime.datetime.now() - last_tweet_time).total_seconds() >= 900):

            tweet_message = (str(formatted_ticket_amount) + " available: " + title_event.title())
            
            print(tweet_message) # This prints to a log file so that I can monitor for errors and such
            type_email = "tickets"
            text_notification.send_email(str(event_date), title_event.title(), str(formatted_ticket_amount), url, type_email,)

            # Update the last tweet time in the database
            update_query = "UPDATE events SET last_tweet = %s WHERE url = %s"
            cursor.execute(update_query, (datetime.datetime.now(), url))
            db_connection.commit()

now = datetime.datetime.today()
dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
print("Script ended at " + dt_string + "")
print("------------------------------")

cursor.close()
db_connection.close()
driver.quit()
