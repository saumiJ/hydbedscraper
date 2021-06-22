from typing import List, Dict, Tuple

from hydbedscraper.parsers.helpers.labels import Label
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


def get_soups() -> List[Tuple[Dict[Label, str], t_BeautifulSoup]]:
    icu_ventilator_bed_table_id = 22
    icu_non_ventilator_bed_table_id = 32
    isolation_oxygen_bed_table_id = 42
    isolation_non_oxygen_bed_table_id = 52

    soups: List[Tuple[Dict[Label, str], t_BeautifulSoup]] = list()

    for table_id,  in [icu_ventilator_bed_table_id, icu_non_ventilator_bed_table_id, isolation_oxygen_bed_table_id, isolation_non_oxygen_bed_table_id]:
        bed_soups.append(soupify_page(base_URL, params={"tid": table_id}))

    return bed_soups
