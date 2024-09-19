import urllib.parse as u


def clean_url(url: str) -> str:
    """
    Removes any query parameters and fragments from the url
    :param url: The url that's fragment and query parameters are being removed
    :return: The cleaned url
    """
    url = u.urlparse(url)
    url = url._replace(fragment="")._replace(query="")
    return url.geturl()


def remove_fragment(url: str) -> str:
    """
    Removes the fragment from the url if there is any
    :param url: The url that the fragment is being removed from
    :return: The url without the fragment
    """
    url = u.urlparse(url)
    url = url._replace(fragment="")
    return url.geturl()


def is_internal_parsed(parsed_base: u.ParseResult, parsed_url: u.ParseResult) -> bool:
    """
    Compares two parsed urls to see if they are part of the same website
    :param parsed_base: The url to be compared
    :param parsed_url: The other url to be compared
    :return: If the urls are part of the same website
    """
    if (parsed_base.netloc == parsed_url.netloc) and (parsed_base.scheme == parsed_url.scheme):
        return True
    return False


def is_internal_link(base_url: str, url: str) -> bool:
    """
    Compares two urls to see if they are part of the same website
    :param base_url: The url to be compared
    :param url: The other url to be compared
    :return: If the urls are part of the same website
    """
    parsed_base = u.urlparse(base_url)
    parsed_url = u.urlparse(url)
    return is_internal_parsed(parsed_base, parsed_url)
