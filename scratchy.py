import bs4
import requests
from collections import deque
from soup import get_internal_urls

try:
    from lxml import etree
    PARSER = 'lxml'
except ImportError:
    PARSER = 'html.parser'

__all__ = ['internal_scrape']

def _internal_scrape(start_url: str, url_queue: deque, visited_urls: set):
    """
    Gets all the internal links in a webpage.

    :param start_url: The url whos domain will be compared to the other links scraped.
    :param url_queue: The queue of urls that need to be scraped.
    :param visited_urls: The set of urls that have already been visited.
    """
    cur_url = url_queue.popleft()
    try:
        res = requests.get(cur_url)
        res.raise_for_status()
    except Exception as e:
        print(f"! Error: {e}")
        visited_urls.add(cur_url)
        return
    visited_urls.add(cur_url)
    soup = bs4.BeautifulSoup(res.text, PARSER)
    print(f"Scraping: {cur_url}")
    urls = get_internal_urls(start_url, soup)
    for url in urls:
        if (url not in visited_urls) and (url not in url_queue):
            # Add the url to the queue
            url_queue.append(url)


def internal_scrape(start_url: str, max_urls: int = None) -> set:
    """
    Gets all the internal links in a website.
    :param start_url: The url to start scraping from.
    :param max_urls: The max number of urls to visit. If unspecified, no limit is set.
    :return: A set of all the internal links in the website.
    """
    url_queue = deque([start_url])
    visited_urls = set()
    if max_urls is None:
        while len(url_queue) != 0:
            _internal_scrape(start_url, url_queue, visited_urls)
    else:
        while len(url_queue) != 0 and len(visited_urls) < max_urls:
            _internal_scrape(start_url, url_queue, visited_urls)
    return visited_urls
