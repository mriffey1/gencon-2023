import smtplib, ssl
from dotenv import load_dotenv
import os
import tweepy
import datetime

load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
send_to_email = os.getenv("SENT_TO_EMAIL")


def send_email(event_datetime, event_title, ticket_amount, event_url, email_type):
    s = smtplib.SMTP("smtp.gmail.com", 587)

    s.starttls()

    s.login(email, password)

    message = f"To: {send_to_email} \n\n{event_title}\n{ticket_amount} {email_type}\n{event_datetime}\n{event_url} \n".encode()

    s.sendmail("sender_email_id", send_to_email, message)

    s.quit()
