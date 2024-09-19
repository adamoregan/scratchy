import bs4
import requests
import urlutil as ut
import urllib.parse as u
from collections import deque

try:
    from lxml import etree
    PARSER = 'lxml'
except ImportError:
    PARSER = 'html.parser'

# SITEMAP_EXTS = (".txt", ".xml")
# TODO: Implement generate_sitemap function


def internal_scrape(start_url: str) -> set:
    """
    Gets all the internal links in a website
    :param start_url: The url to start scraping from
    :return: A set of all the internal links in the website
    """
    parsed_start = u.urlparse(start_url)
    url_queue = deque([start_url])
    visited_urls = set()
    while len(url_queue) != 0:
        cur_url = url_queue.popleft()
        try:
            res = requests.get(cur_url)
            res.raise_for_status()
        except Exception as e:
            print(f"! Error: {e}")
            visited_urls.add(cur_url)
            continue
        visited_urls.add(cur_url)
        soup = bs4.BeautifulSoup(res.text, PARSER)
        print(f"Scraping: {cur_url}")
        # Get all links on a page
        for a in soup.find_all("a", href=True):
            # Create an absolute url from a relative url
            cur_internal_url = u.urljoin(cur_url, a['href'])
            cur_internal_url = ut.remove_fragment(cur_internal_url)
            parsed_cur_internal = u.urlparse(cur_internal_url)
            # Check if it is an internal link
            if ut.is_internal_parsed(parsed_start, parsed_cur_internal):
                # If the url is not already in the queue and not in the visited links
                if (cur_internal_url not in url_queue) and (cur_internal_url not in visited_urls):
                    # Add the url to the queue
                    url_queue.append(cur_internal_url)
    return visited_urls
