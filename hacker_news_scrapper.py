# pylint: disable=missing-module-docstring
import smtplib
import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

from bs4 import BeautifulSoup


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
    # attr = {'class': 'title', 'valign':' ' })):# 'a': 'storylink'
    for i, tag in enumerate(soup.find_all('td', {'class': 'title', 'valign': ''})):
        cnt += ((str(i+1) + ' :: ' + tag.text + "\n" + '<br>')
                if tag.text != 'More' else '')
    return cnt


CNT = extract_news('https://news.ycombinator.com/')
print(CNT)
CONTENT += CNT

CONTENT += ('<br>------<br>')
CONTENT += ('<br><br> End of message')

print('Composing Email...')

# email credentials
SERVER = 'smtp.gmail.com'
PORT = 587
FROM = '<Email-you-send-from>@whatever.com'
TO = '<Email=you-send-to>@whatever.com'
# if using gmail set up 2 factor / app password and use that
PASS = 'password for from email'

msg = MIMEMultipart()

msg["Subject"] = 'Top News Stories HN [Automated email]' + '' + \
    str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO
msg.attach(MIMEText(CONTENT, 'html'))

print('Initiating Server ..')

server = smtplib.SMTP(SERVER, PORT)
#server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print("Email sent")

server.quit()
