from hydbedscraper.parsers.ahmedabad import parse_hospital_tables
from hydbedscraper.requesters.ahmedabad import get_hospital_tables
from hydbedscraper.types import t_DataFrame
from hydbedscraper.writer import to_dataframe


def work() -> t_DataFrame:
    tables = get_hospital_tables()
    info_dict = parse_hospital_tables(tables)
    return to_dataframe(info_dict)
