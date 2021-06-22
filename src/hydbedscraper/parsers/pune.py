import re

from collections import defaultdict
from typing import List, Union, Dict

from hydbedscraper.parsers.helpers.labels import Label
from hydbedscraper.types import t_BeautifulSoup, t_Tag

MSG_LAYOUT_CHANGED = "layout changed, investigate"
NOT_AVAILABLE = "NA"


def _parse_first_string_from_cell(cell: t_Tag) -> str:
    return list(cell.strings)[0]


def _get_occupied_bed_count_from_total_and_vacant(total: int, vacant: int) -> int:
    assert total >= vacant, MSG_LAYOUT_CHANGED
    return total - vacant


_pfsfc = _parse_first_string_from_cell
_to2v = _get_occupied_bed_count_from_total_and_vacant


def parse_soups(soups: List[t_BeautifulSoup]) -> Dict[Label, List[Union[str, int]]]:
    num_columns = 17
    # regex explanation: https://regex101.com/r/RLDkL7/1
    date_time_regex = r".*Last Updated.*Date: *(\d+\/\d+\/\d+)* *(\d+\:\d+\:\d+)*"

    info_dict: Dict[Label, List[Union[str, int]]] = defaultdict(list)
    for soup in soups:
        rows = soup("tr")
        for row in rows:
            cells = row("td")
            if len(cells) != num_columns:
                continue

            info_dict[Label.DISTRICT].append(_pfsfc(cells[1]))
            info_dict[Label.AREA].append(_pfsfc(cells[2]))
            info_dict[Label.HOSPITAL_CATEGORY].append(_pfsfc(cells[3]))

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

            info_dict[Label.HOSPITAL_NAME].append(hospital_name)
            info_dict[Label.HOSPITAL_ADDRESS].append(hospital_address)
            info_dict[Label.CONTACT_NUMBER].append(hospital_phone_number)
            info_dict[Label.LAST_UPDATED_DATE].append(last_updated_date)
            info_dict[Label.LAST_UPDATED_TIME].append(last_updated_time)

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

            info_dict[Label.OFFICER_NAME].append(official_name)
            info_dict[Label.OFFICER_DESIGNATION].append(designation)

            info_dict[Label.CHARGES_TYPE].append(_pfsfc(cells[6]))
            info_dict[Label.FEE_REGULATED_BEDS].append(int(_pfsfc(cells[7])))
            covid19_total_beds = int(_pfsfc(cells[8]))

            isolation_total_beds = int(_pfsfc(cells[9]))
            isolation_vacant_beds = int(_pfsfc(cells[10]))
            isolation_occupied_beds = _to2v(isolation_total_beds, isolation_vacant_beds)
            info_dict[Label.ISOLATION_NON_OXYGEN_OCCUPIED_BEDS].append(
                isolation_occupied_beds
            )
            info_dict[Label.ISOLATION_NON_OXYGEN_VACANT_BEDS].append(
                isolation_vacant_beds
            )

            ventilator_total_beds = int(_pfsfc(cells[11]))
            ventilator_vacant_beds = int(_pfsfc(cells[12]))
            ventilator_occupied_beds = _to2v(
                ventilator_total_beds, ventilator_vacant_beds
            )
            info_dict[Label.ISOLATION_OXYGEN_OCCUPIED_BEDS].append(
                ventilator_occupied_beds
            )
            info_dict[Label.ISOLATION_OXYGEN_VACANT_BEDS].append(ventilator_vacant_beds)

            icu_non_ventilator_total_beds = int(_pfsfc(cells[13]))
            icu_non_ventilator_vacant_beds = int(_pfsfc(cells[14]))
            icu_non_ventilator_occupied_beds = _to2v(
                icu_non_ventilator_total_beds, icu_non_ventilator_vacant_beds
            )
            info_dict[Label.ICU_NON_VENTILATOR_OCCUPIED_BEDS].append(
                icu_non_ventilator_occupied_beds
            )
            info_dict[Label.ICU_NON_VENTILATOR_VACANT_BEDS].append(
                icu_non_ventilator_vacant_beds
            )

            icu_ventilator_total_beds = int(_pfsfc(cells[15]))
            icu_ventilator_vacant_beds = int(_pfsfc(cells[16]))
            icu_ventilator_occupied_beds = _to2v(
                icu_ventilator_total_beds, icu_ventilator_vacant_beds
            )
            info_dict[Label.ICU_VENTILATOR_OCCUPIED_BEDS].append(
                icu_ventilator_occupied_beds
            )
            info_dict[Label.ICU_VENTILATOR_VACANT_BEDS].append(
                icu_ventilator_vacant_beds
            )

            assert (
                covid19_total_beds
                == isolation_total_beds
                + ventilator_total_beds
                + icu_non_ventilator_total_beds
                + icu_ventilator_total_beds
            ), MSG_LAYOUT_CHANGED

    return info_dict
