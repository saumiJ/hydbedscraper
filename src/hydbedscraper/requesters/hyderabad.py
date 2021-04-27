from urllib.parse import urljoin

from hydbedscraper.requesters._common import soupify_page
from hydbedscraper.types import t_BeautifulSoup

base_URL = "http://164.100.112.24/SpringMVC/"


def get_government_hospitals_page_soup() -> t_BeautifulSoup:
    return soupify_page(
        url=urljoin(base_URL, "getHospital_Beds_Status_Citizen.htm"),
        data={"hospital": "G"},
    )


def get_private_hospitals_page_soup() -> t_BeautifulSoup:
    return soupify_page(
        url=urljoin(base_URL, "getHospital_Beds_Status_Citizen.htm"),
        data={"hospital": "P"},
    )
