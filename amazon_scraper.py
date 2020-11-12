#! python3
# amazon_scraper.py - Track Amazon prices and send email

import requests
from bs4 import BeautifulSoup
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

def check_price(URL, threshold_amt):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text().strip()
    price = soup.find(id="priceblock_ourprice").get_text().strip()[1:]
    converted_price = float(price)

    if converted_price < threshold_amt:
        send_mail(URL, title)

    print(f"Item: {title}")
    print(f"Price: {price}")

def send_mail(URL, title):
    subject = "Price fell down for " + title
    body = "Check the Amazon link: " + URL
    sender_email = str(input("Enter sender email: "))
    receiver_email = str(input("Enter recipient email: "))
    password = str(input("Please enter password: "))

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach body to email and convert message to string
    message.attach(MIMEText(body, "plain"))
    msg = message.as_string()

    # Create a secure SSL context and send email
    context = ssl.create_default_context()

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()

    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg)

    print("\nEmail has been sent!")

    server.quit()

if __name__ == "__main__":
    while True:
        check_price("ENTER URL OF AMAZON ITEM", 999) # Set your own URL and threshold amount
        # time.sleep(60 * 60 * 24) # Uncomment and set how often to check prices