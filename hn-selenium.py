# pylint: disable=missing-module-docstring

import smtplib
import datetime
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DRIVER_PATH = '/Users/tonypittella/Desktop/Pet_Projects/Scrapper_hacker-news/chromedriver'
options = Options()
driver = webdriver.Chrome(DRIVER_PATH, options=options)

time.sleep(5)

now = datetime.datetime.now()
CONTENT = " "


def extract_news_selenium(url):
    """
    Uses selenium to scrape
    """
    print("Lets see what we got...")
    cnt = ''
    cnt += ('<b> Hacker News Top Stories </b> \n' +
            '<br>' + '-' * 50 + '<br>\n')
    driver.get(url)
    for i, tag in enumerate(driver.find_elements_by_class_name('storylink')):
        i += 1
        cnt += (str(i) + "-:-" + tag.text + "\n" + '<br>')
    return cnt


CNT = extract_news_selenium('https://news.ycombinator.com/')

CONTENT += CNT

CONTENT += ('<br>------<br>')
CONTENT += ('End of message')

print('Composing Email...')

SERVER = 'smtp.gmail.com'
PORT = 587
FROM = '<your_from_@email.com>'
TO = '<your_to_@email.com>'
PASS = '<app password goes here>'

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

print("Email sent")

server.quit()

driver.quit()