from os.path import splitext, isdir
from fileutil import unique_me
import xml.etree.ElementTree as ET  # writing XML

__all__ = ['create_sitemap']

SUPPORTED_EXTS = (".txt", ".xml")
SITEMAP_URL_LIMIT = 50000
ENCODING = "utf-8"
DEFAULT_FILENAME = "sitemap"


def _write_txt(sitemap_file, urls: set[str]) -> set[str]:
    """
    Writes urls to a .txt sitemap file.
    :param sitemap_file: The .txt sitemap file to be written to.
    :param urls: The urls to be written to the file.
    :return A set of the urls that were written to the file.
    """
    num_urls_written = 0
    written_urls = set()
    for url in urls:
        sitemap_file.write(f"{url}\n")
        num_urls_written += 1
        written_urls.add(url)
    return written_urls


def _write_xml(sitemap_file, urls: set[str]) -> set[str]:
    """
    Writes urls to a .xml sitemap file in binary.
    :param sitemap_file: The .xml sitemap file to be written to.
    :param urls: The urls to be written to the file.
    :return A set of the urls that were written to the file.
    """
    num_urls_written = 0
    written_urls = set()
    root = ET.Element("urlset")
    root.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    for url in urls:
        if num_urls_written >= SITEMAP_URL_LIMIT:
            break
        url_elm = ET.SubElement(root, "url")
        loc_elem = ET.SubElement(url_elm, "loc")
        loc_elem.text = url
        num_urls_written += 1
        written_urls.add(url)
    tree = ET.ElementTree(root)
    ET.indent(tree)  # Readability
    try:
        tree.write(sitemap_file, encoding=ENCODING, xml_declaration=True)
    except Exception as e:
        raise RuntimeError(f"Failed to write XML: {e}")
    return written_urls


def _write_sitemap_file(sitemap_file, urls: set[str], ext: str) -> set[str]:
    """
    Writes urls into a sitemap file of .txt or .xml format.
    :param sitemap_file: The file to write the urls to.
    :param urls: The urls to write to the file.
    :param ext: The extension to determine the output.
    :return A set of the urls that were writen to the .txt file or the .xml file.
    """
    if ext == ".xml":
        return _write_xml(sitemap_file, urls)
    return _write_txt(sitemap_file, urls)


def create_sitemap(urls: set[str], path: str = "", ext: str = ".txt", overwrite: bool = True) -> set[str]:
    """
    Creates a sitemap file in .txt or .xml format at a given path (if specified).

    Enforces an url limit, and returns any leftover urls.
    Be default, creates a .txt sitemap in the current working directory.

    :param urls: The urls to be written to the sitemap file. Accepted as a set to ensure unique values.
    :param path: The path to create the sitemap at. Supports directory paths and file paths.
    If a directory path is given, creates a file with the DEFAULT_FILENAME.
    :param ext: The extension of the desired sitemap.<br>
    If a file path is given, the ext argument becomes redundant.
    :param overwrite: If file overwriting is allowed.<br>
    If false, creates a unique file with windows style naming convention <strong>e.g.</strong> file(1).txt
    :return: The urls that were not written to the file due to the url limit.
    Or an empty set if all urls are written to the file.
    """
    if not urls:
        return set()
    # If path is a directory or not provided, construct default filename
    if not path or isdir(path):
        path = f"{path}{DEFAULT_FILENAME}{ext}"
    else:
        ext = splitext(path)[1]
    if ext not in SUPPORTED_EXTS:
        raise ValueError(f"Unsupported file extension: {ext}")
    # Creates unique filename if overwriting is not allowed
    if not overwrite:
        path = unique_me(path)
    # Sets the write mode based on the file extension
    write_mode = "wb" if ext == ".xml" else "w"
    try:
        with open(path, write_mode, encoding=None if ext == ".xml" else ENCODING) as sitemap_file:
            written_urls = _write_sitemap_file(sitemap_file, urls, ext)
    except OSError as e:
        raise RuntimeError(f"Failed to create file at {path}: {e}")
    if len(urls) <= SITEMAP_URL_LIMIT:
        leftover_urls = set()
    else:
        leftover_urls = urls - written_urls  # O(N)
    return leftover_urls
