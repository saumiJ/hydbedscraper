from hydbedscraper.parsers.hyderabad import (
    parse_government_hospitals,
    parse_private_hospitals,
)
from hydbedscraper.requesters.hyderabad import (
    get_government_hospitals_page_soup,
    get_private_hospitals_page_soup,
)
from hydbedscraper.types import t_DataFrameDict
from hydbedscraper.writers.hyderabad import to_dataframe_dict


def work() -> t_DataFrameDict:
    govt_soup = get_government_hospitals_page_soup(use_test=False)
    private_soup = get_private_hospitals_page_soup(use_test=False)

    govt_info = parse_government_hospitals(govt_soup)
    private_info = parse_private_hospitals(private_soup)

    return to_dataframe_dict(govt_info, private_info)
