import requests
import smtplib
from email.message import EmailMessage
import time
import random
import os
from dotenv import load_dotenv

load_dotenv()

STOCK_NAME = os.getenv("STOCK_NAME", "TSLA")
COMPANY_NAME = os.getenv("COMPANY_NAME", "Tesla Inc")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
STOCK_API_KEY = os.getenv("STOCK_API_KEY")
STOCK_ENDPOINT = os.getenv("STOCK_ENDPOINT", "https://www.alphavantage.co/query?")
NEWS_ENDPOINT = os.getenv("NEWS_ENDPOINT", "https://newsapi.org/v2/everything")
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")


stock_paramaters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

news_paramaters = {
    "qInTitle": COMPANY_NAME,
    "apiKey": NEWS_API_KEY
}

news_response = requests.get(url=NEWS_ENDPOINT,params=news_paramaters)

news_data = news_response.json()

r = requests.get(url=STOCK_ENDPOINT,params=stock_paramaters)

data = r.json()

daily_data = data["Time Series (Daily)"]

stock_data = [value for (key,value) in daily_data.items()]

yesterday_close = float(stock_data[0]["4. close"])

day_before_yesterday_close = float(stock_data[1]["4. close"])

difference = yesterday_close - day_before_yesterday_close

up_down = None

if difference > 0:
    up_down = "↑"
else:
    up_down = "↓"

percentage_difference = round((difference / day_before_yesterday_close) * 100,2)

if abs(percentage_difference) > 5:

    articles = news_data["articles"]

    random_article = random.choice(articles)

    formatted_article = (
    f"Headline: {up_down}{percentage_difference}% {random_article['title']}\n\n"
    f"Brief: {random_article['description']}"
    )

    print(formatted_article)
    
    msg = EmailMessage()
    msg["Subject"] = "TESLA Borsa Güncel Durumu"
    msg["From"] = MY_EMAIL
    msg["To"] = RECIPIENT_EMAIL  

    msg.set_content(formatted_article)

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        print("Bağlaniyor...")
        connection.starttls()
        print("TLS OK")
        connection.login(MY_EMAIL, MY_PASSWORD)  
        print("Login OK")
        connection.send_message(msg=msg, from_addr=MY_EMAIL, to_addrs=RECIPIENT_EMAIL)
        print("Email gönderildi")
        time.sleep(5)
        





