from typing import List
from urllib.parse import urljoin

from hydbedscraper.requesters._common import soupify_page
from hydbedscraper.types import t_BeautifulSoup

base_URL = "https://www.divcommpunecovid.com/ccsbeddashboard/"


def _get_url_list_of_all_information_pages(source_soup: t_BeautifulSoup) -> List[str]:
    # find element containing page-links
    page_links_elements = source_soup.select("span[class*=pagelink]")
    assert (
        len(page_links_elements) == 1
    ), f"number of page-link elements has changed, please investigate source"
    page_links_element = page_links_elements[0]
    # find page-links
    page_links = page_links_element.select("a[href]")
    url_set = {urljoin(base_URL, page_link["href"]) for page_link in page_links}
    return list(url_set)


def get_soups() -> List[t_BeautifulSoup]:
    source_soup = soupify_page(url=urljoin(base_URL, "hsr"))
    url_list = _get_url_list_of_all_information_pages(source_soup)
    return [soupify_page(url=url) for url in url_list]
