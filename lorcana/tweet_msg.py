import tweepy
import datetime
import utils_lorcana

dbhost, dbusername, dbpassword, dbname = utils_lorcana.database_stuff()

tbearer, tckey, tcsecret, tatoken, tasecret = utils_lorcana.twitter_stuff()


def send_email(event_datetime, event_title, ticket_amount, event_url, email_type):
    if "Lorcana" in event_title:
        api = tweepy.Client(
            bearer_token=tbearer,
            consumer_key=tckey,
            consumer_secret=tcsecret,
            access_token=tatoken,
            access_token_secret=tasecret,
        )
        now = datetime.datetime.today()
        dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
        # authentication of consumer key and secret
        tweet = api.create_tweet(
            text=f"{event_title}\n{event_datetime}\n{ticket_amount} ticket(s)\n{event_url}\nChecked {dt_string}",
        )
    else:
        print("No tickets")
