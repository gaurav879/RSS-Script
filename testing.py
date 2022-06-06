"""
Testing file for task.py
"""

import requests
from bs4 import BeautifulSoup
import feedparser

URL = "https://www.wired.com/feed/category/business/latest/rss"


def test_get_updated_feed():
    """
    Test for get_updated_feed function
    """
    parsed_data = feedparser.parse(URL)

    assert "entries" in parsed_data.keys()
    assert len(parsed_data) > 0
    assert "title" in parsed_data.entries[0]
    assert "link" in parsed_data.entries[0]
    assert "published" in parsed_data.entries[0]
    assert "summary" in parsed_data.entries[0]
    assert "author" in parsed_data.entries[0]
    page = requests.get(parsed_data.entries[0].link)
    page_content = BeautifulSoup(page.content, "html.parser")
    _title = page_content.find(
        class_="BaseWrap-sc-TURhJ BaseText-fFzBQt ContentHeaderHed-kpvpFG eTiIvU bVPdwx kjQZOs"
    ).text
    assert parsed_data.entries[0].title == _title
