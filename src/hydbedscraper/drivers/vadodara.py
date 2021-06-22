from hydbedscraper.parsers.vadodara import parse_soups
from hydbedscraper.requesters.vadodara import (
    get_soups,
)
from hydbedscraper.types import t_DataFrame
from hydbedscraper.writer import to_dataframe


def work() -> t_DataFrame:
    soups = get_soups()
    info_dict = parse_soups(soups)

    return to_dataframe(info_dict)
