from typing import List, Dict, Tuple
from urllib.parse import urljoin

from hydbedscraper.parsers.helpers.labels import Label
from hydbedscraper.requesters._common import soupify_page
from hydbedscraper.types import t_BeautifulSoup

base_URL = "http://164.100.112.24/SpringMVC/"


def get_soups() -> List[Tuple[Dict[Label, str], t_BeautifulSoup]]:
    soups: List[Tuple[Dict[Label, str], t_BeautifulSoup]] = list()
    government_hospital_param = "G"
    private_hospital_param = "P"

    for param, charges_type in [
        (government_hospital_param, "Free"),
        (private_hospital_param, "Chargeable"),
    ]:
        label_to_value_dict = {Label.CHARGES_TYPE: charges_type}
        soup = soupify_page(
            url=urljoin(base_URL, "getHospital_Beds_Status_Citizen.htm"),
            data={"hospital": param},
        )
        soups.append((label_to_value_dict, soup))

    return soups
