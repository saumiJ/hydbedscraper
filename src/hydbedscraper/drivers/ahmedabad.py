from hydbedscraper.parsers.ahmedabad import parse_hospital_tables
from hydbedscraper.requesters.ahmedabad import get_hospital_tables
from hydbedscraper.writers.ahmedabad import to_dataframe_dict


def work():
    tables = get_hospital_tables()
    hospital_category_to_information_dict = parse_hospital_tables(tables)
    return to_dataframe_dict(hospital_category_to_information_dict)
