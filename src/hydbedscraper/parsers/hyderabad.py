import logging
from collections import defaultdict

from typing import Dict, List, Tuple

from hydbedscraper.types import t_BeautifulSoup
from hydbedscraper.parsers.helpers.labels import Label


def parse_soups(
    soups: List[Tuple[Dict[Label, str], t_BeautifulSoup]]
) -> Dict[Label, list]:
    info_dict: Dict[Label, list] = defaultdict(list)
    for param_dict, soup in soups:
        col_id_of_district = 1
        label_colid_dtype = [
            (Label.HOSPITAL_NAME, 2, str),
            (Label.CONTACT_NUMBER, 3, str),
            (Label.ISOLATION_NON_OXYGEN_OCCUPIED_BEDS, 5, int),
            (Label.ISOLATION_NON_OXYGEN_VACANT_BEDS, 6, int),
            (Label.ISOLATION_OXYGEN_OCCUPIED_BEDS, 8, int),
            (Label.ISOLATION_OXYGEN_VACANT_BEDS, 9, int),
            (Label.ICU_VENTILATOR_OCCUPIED_BEDS, 11, int),
            (Label.ICU_VENTILATOR_VACANT_BEDS, 12, int),
            (Label.LAST_UPDATED_DATE, 16, str),
            (Label.LAST_UPDATED_TIME, 17, str),
        ]
        table = soup.find("table")
        body = table.find("tbody")
        rows = body("tr")
        current_district: str = ""
        for row in rows:
            cells = row("td")
            # check if start of new district
            if len(cells) > 16:
                assert "rowspan" in cells[col_id_of_district].attrs
                current_district = cells[col_id_of_district].string
                offset = 0
            else:
                offset = -2
            info_dict[Label.DISTRICT].append(current_district)
            for label, col_id, dtype in label_colid_dtype:
                info_dict[label].append(dtype(cells[col_id + offset].string.strip()))
            for label, value in param_dict.items():
                info_dict[label].append(value)
    return info_dict
