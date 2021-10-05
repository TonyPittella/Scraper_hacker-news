# pylint: disable=all
import smtplib
import os
import pytest
import requests
from dotenv import load_dotenv
from hacker_news_scrapper import URL, BeautifulSoup

load_dotenv()
SERVER = os.getenv('SERVER')
PORT = os.getenv('PORT')
FROM = os.getenv('FROM')
PASS = os.getenv('PASS')


@pytest.fixture
def page_url():
    """
    tests url 
    """
    req = requests.get(URL)
    return req


@pytest.fixture
def page_html(page_url):
    """
    tests beautifulsoup parser
    """
    soup = BeautifulSoup(page_url.content, "html.parser")
    return soup


@pytest.fixture
def email_server_ping():
    """
    test email ping
    """
    server = smtplib.SMTP(SERVER, PORT)
    server.set_debuglevel(True)
    server.ehlo()
    server.starttls()
    server.login(FROM, PASS)
    try:
        server.verify(FROM)
        return True
    except Exception:
        return False
    finally:
        server.quit()
