from os.path import splitext, isdir
from fileutil import unique_me

__all__ = ['create_sitemap']
SUPPORTED_EXTS = (".txt", ".xml")
SITEMAP_URL_LIMIT = 50000


def _write_txt(sitemap_file, urls: set) -> None:
    """
    Writes urls to a .txt sitemap file.
    :param sitemap_file: The .txt sitemap file to be written to.
    :param urls: The urls to be written to the file.
    """
    num_urls_written = 0
    while num_urls_written < SITEMAP_URL_LIMIT and len(urls) > 0:  # O(1) for set len
        current_url = urls.pop()  # O(1)
        sitemap_file.write(current_url + "\n")
        num_urls_written += 1


def _write_xml(sitemap_file, urls: set) -> None:
    num_urls_written = 0
    xml_format = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    sitemap_file.write(xml_format + "\n")
    xml_format = "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"
    sitemap_file.write(xml_format + "\n")
    url_tag_open, url_tag_close = "  <url>", "  </url>"
    while num_urls_written < SITEMAP_URL_LIMIT and len(urls) > 0:
        current_url = urls.pop()  # O(1)
        sitemap_file.write(url_tag_open + "\n")
        loc = f"    <loc>{current_url}</loc>"
        sitemap_file.write(loc + "\n")
        sitemap_file.write(url_tag_close + "\n")
    xml_format = "</urlset>"
    sitemap_file.write(xml_format)


def _write_sitemap(sitemap_file, urls: set, ext: str) -> None:
    """
    Writes urls into a sitemap file of a specific extension.
    :param sitemap_file: The file to write the urls to.
    :param urls: The urls to write to the file.
    :param ext: The extension of the sitemap file.
    """
    if ext == ".xml":
        _write_xml(sitemap_file, urls)
    else:
        _write_txt(sitemap_file, urls)


def create_sitemap(urls: set, path: str = "", ext: str = ".txt", overwrite: bool = True) -> set:
    """
    Creates a sitemap file in .txt or .xml format at a given path (if specified).

    Enforces an url limit, and returns any leftover urls.
    Be default, creates a .txt sitemap in the current working directory.

    :param urls: The urls to be written to the sitemap file. Accepted as a set to ensure unique values.
    :param path: The path to create the sitemap at. Supports directory paths and file paths.
    :param ext: The extension of the desired sitemap.<br>
    If a file path is given, the ext argument becomes redundant.
    :param overwrite: If file overwriting is allowed.<br>
    If false, creates a unique file with windows style naming convention <strong>e.g.</strong> file(1).txt
    :return: The urls that were not written to the file due to the url limit.
    Or an empty set if all urls are written to the file.
    """
    # By default, creates a file at the cwd.
    # If the user enters a directory, creates the sitemap at that directory.
    if path == "" or isdir(path):
        path += "sitemap" + ext
    # If a file path is given, the extension is checked.
    else:
        ext = splitext(path)[1]
    if ext not in SUPPORTED_EXTS:
        raise ValueError("Valid extension not detected.")
    if not overwrite:
        path = unique_me(path)
    # Justification: To not impact the given urls, since they may be needed for other operations.
    urls = set(urls)
    with open(path, "w") as sitemap:
        _write_sitemap(sitemap, urls, ext)
    return urls  # remaining urls, if any, for additional sitemap creations
