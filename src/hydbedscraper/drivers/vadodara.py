from hydbedscraper.parsers.vadodara import parse_bed_soup
from hydbedscraper.requesters.vadodara import (
    get_icu_ventilator_bed_soup,
    get_icu_non_ventilator_bed_soup,
    get_oxygen_bed_soup,
    get_normal_bed_soup,
)
from hydbedscraper.types import t_DataFrameDict
from hydbedscraper.writers.vadodara import to_dataframe_dict


def work() -> t_DataFrameDict:
    icu_ventilator_soup = get_icu_ventilator_bed_soup()
    icu_non_ventilator_soup = get_icu_non_ventilator_bed_soup()
    oxygen_bed_soup = get_oxygen_bed_soup()
    normal_bed_soup = get_normal_bed_soup()

    icu_ventilator_bed_info = parse_bed_soup(icu_ventilator_soup)
    icu_non_ventilator_bed_info = parse_bed_soup(icu_non_ventilator_soup)
    oxygen_bed_info = parse_bed_soup(oxygen_bed_soup)
    normal_bed_info = parse_bed_soup(normal_bed_soup)

    return to_dataframe_dict(
        icu_ventilator_bed_info,
        icu_non_ventilator_bed_info,
        oxygen_bed_info,
        normal_bed_info,
    )
