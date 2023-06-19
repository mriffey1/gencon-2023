import os
from dotenv import load_dotenv
from selenium import webdriver

load_dotenv()

def twitter_stuff():
    twit_bearer = os.getenv("BEARER")
    twit_ckey = os.getenv("CONSUMERKEY")
    twit_csecret = os.getenv("CONSUMERSECRET")
    twit_atoken = os.getenv("ACCESSTOKEN")
    twit_asecret = os.getenv("ACCESSSECRET")
    return twit_bearer, twit_ckey, twit_csecret, twit_atoken, twit_asecret

def database_stuff():
    dbhost = os.getenv("HOST")
    dbusername = os.getenv("USER")
    dbpassword = os.getenv("PASSWORD")
    dbname = os.getenv("DATABASE")
    return dbhost, dbusername, dbpassword, dbname

def chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-gpu")
    options.add_argument("--start-maximized")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--enable-javascript")
    return options
