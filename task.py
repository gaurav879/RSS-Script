"""
Module for notifing updates in the RSS feed
"""
import csv
import logging
from datetime import datetime
from typing import Any, Dict, List

import feedparser
import schedule

logging.basicConfig(
    handlers=[logging.FileHandler(filename="./logs.log", encoding="utf-8", mode="a+")],
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s - %(message)s",
)

URL: str = "https://www.wired.com/feed/category/business/latest/rss"


def get_updated_feed(top_id: str) -> str:
    """
    Displays the updated items in the feed with title and link, also updates the id of top most item
    Args:
        top_id(str): Stores the id of top most item
    Returns(str):
        id of top most item from updated feed
    """
    print(datetime.now())
    try:
        # Stores updated RSS feed from URL
        updated_parsed_data: Dict[str, Any] = feedparser.parse(URL)
    except Exception as e:
        logging.error(f"{e}")

    if "entries" in updated_parsed_data.keys():
        for item in updated_parsed_data.entries:
            if item.id != top_id:
                # Displays the updated entries in feed
                print(item.title)
                print(item.link)
                media_keywords: List[str] = item.media_keywords.strip(" ").split(", ")
                # Append data to file
                with open("feed.tsv", "a", newline="") as csvfile:
                    spamwriter = csv.writer(
                        csvfile,
                        delimiter="\t",
                        quotechar="|",
                        quoting=csv.QUOTE_MINIMAL,
                    )
                    for keyword in media_keywords:
                        spamwriter.writerow([keyword, item.link, item.author])
                logging.info(
                    f"""{item.title} | {item.link} | {item.published} |
                     {item.summary} | {item.author}"""
                )
            else:
                break
        # Returns the id of top most item in feed
        return updated_parsed_data.entries[0].id
    return top_id


def get_top_id() -> None:
    """
    Updates and stores id of top most item from feed
    Args:
        None
    Returns:
        None
    """
    global top_id
    top_id = get_updated_feed(top_id)


if __name__ == "__main__":
    # Get initial RSS feed from site
    print("Script has started running...")
    parsed_data: Dict[str, Any] = feedparser.parse(URL)
    top_id: str = parsed_data.entries[0].id
    # Creating a TSV file for storing the updated data
    with open("feed.tsv", "w", newline="") as csvfile:
        spamwriter = csv.writer(
            csvfile, delimiter="\t", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        # Add heading to file
        spamwriter.writerow(["Keyword"] + ["Article"] + ["Author"])
    media_keywords = parsed_data.entries[0].media_keywords.strip(" ").split(", ")
    schedule.every(10).minutes.do(get_top_id)

    while True:
        schedule.run_pending()
