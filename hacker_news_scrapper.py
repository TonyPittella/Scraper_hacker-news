# pylint: disable=missing-module-docstring
import smtplib
import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os

import requests

from bs4 import BeautifulSoup

from dotenv import load_dotenv

now = datetime.datetime.now()
CONTENT = " "

def extract_news(url):
    """
    Grabs the the first 30 new stories from Hacker News
    """
    print("Grabbing first 30 stories...")
    cnt = ''
    cnt += ('<b> Hacker News Top Stories </b> \n' +
            '<br>' + '-' * 50 + '<br>\n')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', {'class': 'title', 'valign': ''})):
        cnt += ((str(i+1) + ' :: ' + tag.text + "\n" + '<br>')
                if tag.text != 'More' else '')
    return cnt

URL = 'https://news.ycombinator.com/'
CNT = extract_news(URL)
CONTENT += CNT

CONTENT += ('<br>------<br>')
CONTENT += ('<br><br> End of message')

print('Composing Email...')
load_dotenv()
SERVER = 'smtp.gmail.com'
PORT = 587
FROM = os.getenv('FROM')
TO = os.getenv('TO')
PASS = os.getenv('PASS')

def send_email():
    """
    compiles message format and sends it
    """
    msg = MIMEMultipart()
    msg["Subject"] = 'Top News Stories HN [Automated email]' + '' + \
        str(now.day) + '-' + str(now.month) + '-' + str(now.year)
    msg['From'] = FROM
    msg['To'] = TO
    msg.attach(MIMEText(CONTENT, 'html'))
    print('Initiating Server ..')
    server = smtplib.SMTP(SERVER, PORT)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(FROM, PASS)
    server.sendmail(FROM, TO, msg.as_string())
    print('*-' * 10 + "Email sent"+ '*-' * 10  )
    server.quit()
send_email()
