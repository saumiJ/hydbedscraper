from collections import defaultdict
from typing import Dict, List, Tuple, Any

from hydbedscraper.parsers.helpers.labels import Label
from hydbedscraper.types import t_BeautifulSoup


def parse_soups(soups: List[Tuple[Label, Label, t_BeautifulSoup]]) -> Dict[Label, list]:
    info_dict: Dict[Label, list] = defaultdict(list)
    hospital_name_to_info_dict_dict: Dict[str, Dict[Label, Any]] = defaultdict(dict)
    hospital_name_id = 0
    for occupied_bed_label, vacant_bed_label, soup in soups:
        label_colid_dtype = [
            (Label.HOSPITAL_ADDRESS, 1, str),
            (occupied_bed_label, 3, int),
            (vacant_bed_label, 4, int),
            (Label.OFFICER_NAME, 5, str),
            (Label.CONTACT_NUMBER, 6, str),
        ]
        rows = soup("tr")
        num_columns = 8
        for row in rows:
            cells = row("td")
            if len(cells) != num_columns:
                continue
            hospital_name = str(cells[hospital_name_id].string).strip().lower()
            for label, col_id, _type in label_colid_dtype:
                hospital_name_to_info_dict_dict[hospital_name][label] = _type(
                    cells[col_id].string
                )
    for hospital_name, _info_dict in hospital_name_to_info_dict_dict.items():
        for label in [
            Label.ICU_VENTILATOR_OCCUPIED_BEDS,
            Label.ICU_VENTILATOR_VACANT_BEDS,
            Label.ICU_NON_VENTILATOR_OCCUPIED_BEDS,
            Label.ICU_NON_VENTILATOR_VACANT_BEDS,
            Label.ISOLATION_OXYGEN_OCCUPIED_BEDS,
            Label.ISOLATION_OXYGEN_VACANT_BEDS,
            Label.ISOLATION_NON_OXYGEN_OCCUPIED_BEDS,
            Label.ISOLATION_NON_OXYGEN_VACANT_BEDS,
        ]:
            if label not in _info_dict.keys():
                _info_dict[label] = 0
        info_dict[Label.HOSPITAL_NAME].append(hospital_name)
        for label, val in _info_dict.items():
            info_dict[label].append(val)
    return info_dict
