# pylint: disable=missing-module-docstring
import smtplib
import datetime

import sqlite3
from sqlite3 import Error

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os

import requests

from bs4 import BeautifulSoup

from dotenv import load_dotenv

now = datetime.datetime.now()
CONTENT = " "
URL = 'https://news.ycombinator.com/'

load_dotenv()
SERVER = 'smtp.gmail.com'
PORT = 587
FROM = os.getenv('FROM')
TO = os.getenv('TO')
PASS = os.getenv('PASS')

DATE_VARIES = str(now.day) + '-' + str(now.month) + '-' + str(now.year)


def extract_news(url):
    """
    Grabs the the first 30 new stories from Hacker News
    """
    print("Grabbing first 30 stories...")
    cnt = ''
    cnt += ('-|- Hacker News Top Stories -|- \n' +
            '<br>' + '-' * 50 + '<br>\n')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', {'class': 'title', 'valign': ''})):
        cnt += ((str(i+1) + ' :: ' + tag.text + "\n" + '<br>')
                if tag.text != 'More' else '')
    return cnt


CNT = extract_news(URL)
# print(CNT)
print(CNT)
CONTENT += CNT
# CONTENT += ('<br>------<br>')
# CONTENT += ('<br><br> End of message')

# print('Composing Email...')

# def send_email():
#     """
#     compiles message format and sends it
#     """
#     msg = MIMEMultipart()
#     msg["Subject"] = 'Top News Stories HN [Automated email]' + '' + \
#         DATE_VARIES
#     msg['From'] = FROM
#     msg['To'] = TO
#     msg.attach(MIMEText(CONTENT, 'html'))
#     print('Initiating Server ..')
#     server = smtplib.SMTP(SERVER, PORT)
#     server.set_debuglevel(1)
#     server.ehlo()
#     server.starttls()
#     server.login(FROM, PASS)
#     server.sendmail(FROM, TO, msg.as_string())
#     print('*-' * 10 + "Email sent"+ '*-' * 10  )
#     server.quit()
# send_email()

# def create_to_db():
#     """
#     create a database in sqlite3
#     """
#     conn = None
#     try:
#         conn = sqlite3.connect('hn_db.db')
#         print("-!-" *15 + "Ah, so you created a database" + "-!-" * 15)
#         table_made =   """
#                         CREATE TABLE hacker_news(
#                         index_num int,
#                         head_line varcar(160),
#                         source_site varcar(25)
#                         );
#                         """
#         cursor = conn.cursor()
#         print("If your here, then we successfully connected to the DB")
#         cursor.execute(table_made)
#     except Error as e:
#         print("Ruh Roo.....", e)
#     finally:
#         if conn:
#             conn.close()
#     return conn
# create_to_db()

# def string_break_down(CNT):
#     banner1 = CNT.replace('<br>', '').replace(' :: ', ", ").replace('(', ", ").replace(')', " ")
#     #banner2 is a list of strings now don't forget
#     banner2 = banner1.split("\n")
#     entries= []
#     print("stop, drop...")
#     for segment in banner2[2:32]:
#         banner3 = segment.split(',')
#         index_num =banner3[0]
#         head_line = banner3[1]
#         source_site = banner3[2]
#         #print(index_num, head_line, source_site)
#         entries.append((index_num, head_line, source_site))
#     print("shut'em down...")
#     return entries

# broken_strings = string_break_down(CNT)
# #print(broken_strings)
# def add_to_db(broken_strings):
#     """
#     populates sqlite table with scraper output
#     """
#     conn = sqlite3.connect("hn_db.db")
#     print("open up shop..")
#     cur = conn.cursor()
#     cur.executemany("INSERT INTO hacker_news VALUES(?,?,?)", broken_strings)
#     conn.commit()
# add_to_db(broken_strings)
