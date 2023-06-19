import os
from dotenv import load_dotenv

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
