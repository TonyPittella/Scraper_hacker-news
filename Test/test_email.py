from pathlib import Path
import pytest
from hacker_news_scrapper import *


def test_email_connection(email_server_ping):
    assert email_server_ping == True
