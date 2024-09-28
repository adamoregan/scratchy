import bs4
import urlutil as ut
import urllib.parse as u


def get_internal_urls(url: str, soup: bs4.BeautifulSoup) -> set:
    """
    Gets all the internal links in a soup object.

    :param url: The url whose domain is being compared to the links scraped.
    :param soup: The BeautifulSoup that is being parsed to get the internal links.
    :return: A set of all unique internal links in the soup object.
    """
    urls = set()
    parsed_link = u.urlparse(url)
    # Get all links on a page
    for a in soup.find_all("a", href=True):
        # Create an absolute url from a relative url
        cur_internal_url = u.urljoin(url, a['href'])
        cur_internal_url = ut.remove_fragment(cur_internal_url)
        parsed_cur_internal = u.urlparse(cur_internal_url)
        # Check if it is an internal link
        if ut.is_internal_parsed(parsed_link, parsed_cur_internal):
            urls.add(cur_internal_url)
    return urls
