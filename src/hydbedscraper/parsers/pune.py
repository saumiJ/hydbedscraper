import re

from collections import defaultdict
from typing import List, Union, Dict

from hydbedscraper.types import t_BeautifulSoup, t_Tag

MSG_LAYOUT_CHANGED = "layout changed, investigate"
NOT_AVAILABLE = "NA"


def _parse_first_string_from_cell(cell: t_Tag) -> str:
    return list(cell.strings)[0]


_pfsfc = _parse_first_string_from_cell


def parse_bed_soups(bed_soups: List[t_BeautifulSoup]) -> dict:
    num_columns = 17
    # regex explanation: https://regex101.com/r/RLDkL7/1
    date_time_regex = r".*Last Updated.*Date: *(\d+\/\d+\/\d+)* *(\d+\:\d+\:\d+)*"

    info_dict: Dict[str, List[Union[str, int]]] = defaultdict(list)
    for bed_soup in bed_soups:
        rows = bed_soup("tr")
        for row in rows:
            cells = row("td")
            if len(cells) != num_columns:
                continue

            info_dict["district"].append(_pfsfc(cells[1]))
            info_dict["area"].append(_pfsfc(cells[2]))
            info_dict["hospital_category"].append(_pfsfc(cells[3]))

            hospital_details_strings = [
                string for string in cells[4].strings if string != "\n"
            ]
            hospital_name = hospital_details_strings[0]
            assert "address" in hospital_details_strings[1].lower(), MSG_LAYOUT_CHANGED
            hospital_address = hospital_details_strings[2]
            assert "number" in hospital_details_strings[3].lower(), MSG_LAYOUT_CHANGED
            hospital_phone_number = hospital_details_strings[4]
            date_time_string = hospital_details_strings[5]
            assert "last updated" in date_time_string.lower(), MSG_LAYOUT_CHANGED
            regex_result = re.search(date_time_regex, date_time_string)
            if regex_result is None:
                last_updated_date = NOT_AVAILABLE
                last_updated_time = NOT_AVAILABLE
            else:
                last_updated_date = regex_result.group(1)
                last_updated_time = regex_result.group(2)

            info_dict["hospital_name"].append(hospital_name)
            info_dict["hospital_address"].append(hospital_address)
            info_dict["hospital_phone_number"].append(hospital_phone_number)
            info_dict["last_updated_date"].append(last_updated_date)
            info_dict["last_updated_time"].append(last_updated_time)

            officials_strings = [
                string for string in cells[5].strings if string != "\n"
            ]
            assert (
                "officer" in officials_strings[0].lower()
                and "name" in officials_strings[0].lower()
            ), MSG_LAYOUT_CHANGED
            official_name = officials_strings[1]
            assert "designation" in officials_strings[2].lower(), MSG_LAYOUT_CHANGED
            designation = officials_strings[3]

            info_dict["official_name"].append(official_name)
            info_dict["designation"].append(designation)

            info_dict["charges"].append(_pfsfc(cells[6]))
            info_dict["fee_regulated_beds"].append(int(_pfsfc(cells[7])))
            info_dict["total_covid19_bed_capacity"].append(int(_pfsfc(cells[8])))
            info_dict["total_non_oxygen_isolation_beds"].append(int(_pfsfc(cells[9])))
            info_dict["vacant_non_oxygen_isolation_beds"].append(int(_pfsfc(cells[10])))
            info_dict["total_oxygen_isolation_beds"].append(int(_pfsfc(cells[11])))
            info_dict["vacant_oxygen_isolation_beds"].append(int(_pfsfc(cells[12])))
            info_dict["total_non_ventilator_icu_beds"].append(int(_pfsfc(cells[13])))
            info_dict["vacant_non_ventilator_icu_beds"].append(int(_pfsfc(cells[14])))
            info_dict["total_ventilator_icu_beds"].append(int(_pfsfc(cells[15])))
            info_dict["vacant_ventilator_icu_beds"].append(int(_pfsfc(cells[16])))

    return info_dict
