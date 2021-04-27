from hydbedscraper.requesters._common import soupify_page
from hydbedscraper.types import t_BeautifulSoup

base_URL = "https://vmc.gov.in/Covid19VadodaraApp/HospitalBedsDetails.aspx"


def get_icu_ventilator_bed_soup() -> t_BeautifulSoup:
    return soupify_page(
        url=base_URL,
        params={"tid": 22},
    )


def get_icu_non_ventilator_bed_soup() -> t_BeautifulSoup:
    return soupify_page(
        url=base_URL,
        params={"tid": 32},
    )


def get_oxygen_bed_soup() -> t_BeautifulSoup:
    return soupify_page(
        url=base_URL,
        params={"tid": 42},
    )


def get_normal_bed_soup() -> t_BeautifulSoup:
    return soupify_page(
        url=base_URL,
        params={"tid": 52},
    )
