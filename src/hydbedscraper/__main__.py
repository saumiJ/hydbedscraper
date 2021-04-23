import json
import requests

from bs4 import BeautifulSoup

from hydbedscraper.type import t_BeautifulSoup, t_SummaryDict
from hydbedscraper.testdata.path import test_summary_html


def get_base_page_soup(use_test: bool = True) -> t_BeautifulSoup:
    if use_test:
        with open(test_summary_html) as fp:
            soup = BeautifulSoup(fp, "lxml")
    else:
        page = requests.get("http://164.100.112.24/SpringMVC/Hospital_Beds_Statistic_Bulletin_citizen.htm")
        soup = BeautifulSoup(page.content, "lxml")
    return soup


def extract_summary(soup: t_BeautifulSoup) -> t_SummaryDict:
    summary_dict: t_SummaryDict = dict()

    # column-ids
    col_id_of_hospital_type = 1
    col_id_of_regular_beds = 2
    col_id_of_oxygen_beds = 5
    col_id_of_icu_beds = 8

    # offsets
    occupied_offset = 1
    vacant_offset = 2

    # get first instance of table
    summary_table = soup.find("table")

    # populate info
    body = summary_table.find("tbody")
    body_rows = body("tr")
    for bed_type, col_id_of_bed_type in [
        ("regular_bed", col_id_of_regular_beds),
        ("oxygen_bed", col_id_of_oxygen_beds),
        ("icu_bed", col_id_of_icu_beds),
    ]:
        summary_dict[bed_type] = dict()
        for status, status_offset in [
            ("occupied", occupied_offset),
            ("vacant", vacant_offset),
        ]:
            summary_dict[bed_type][status] = dict()
            for row in body_rows:
                row_cols = row("td")
                hospital_type = row_cols[col_id_of_hospital_type].a.string
                summary_dict[bed_type][status][hospital_type] = int(
                    row_cols[col_id_of_bed_type + status_offset].string
                )

    return summary_dict


def main():
    base_soup = get_base_page_soup(use_test=False)
    summary = extract_summary(base_soup)
    with open("summary.json", "w") as fp:
        json.dump(summary, fp, indent=2)


if __name__ == "__main__":
    main()
