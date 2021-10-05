# pylint: disable=all
from pathlib import Path
import pytest
from hacker_news_scrapper import *


def test_email_connection(email_server_ping):
    """
    test email connection
    """
    assert email_server_ping == True
