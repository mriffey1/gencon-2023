from selenium import webdriver
import datetime as datetime
import mysql.connector
import os
from dotenv import load_dotenv

def database_stuff():
    dbhost = os.getenv("HOST")
    dbusername = os.getenv("USER")
    dbpassword = os.getenv("PASSWORD")
    dbname = os.getenv("DATABASE")
    return dbhost, dbusername, dbpassword, dbname

def connect_to_database():
    dbhost, dbusername, dbpassword, dbname = database_stuff()
    db_connection = mysql.connector.connect(host=dbhost, user=dbusername, password=dbpassword, database=dbname)
    cursor = db_connection.cursor()
    return db_connection, cursor

def chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36")
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
