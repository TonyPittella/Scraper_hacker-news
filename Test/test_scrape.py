from pathlib import Path
import pytest
from hacker_news_scrapper import *


def test_html_existence(page_html):
    assert page_html != None


def test_for_tables(page_html):
    title_30 = page_html.find_all('td', {'class': 'title', 'valign': ''})
    assert len(title_30) > 0


def test_url_request(page_url):
    assert page_url.status_code == 200
