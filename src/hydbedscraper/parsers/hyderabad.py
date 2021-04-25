import logging

from hydbedscraper.types import t_BeautifulSoup, t_SummaryDict, t_FullDict


def parse_government_hospitals(govt_soup: t_BeautifulSoup) -> t_FullDict:
    logging.info("parsing hospitals page..")
    col_id_of_district = 1
    key_colid_dtype = [
        ("hospital_name", 2, str),
        ("contact_number", 3, str),
        ("regular_bed_occupied", 5, int),
        ("regular_bed_vacant", 6, int),
        ("oxygen_bed_occupied", 8, int),
        ("oxygen_bed_vacant", 9, int),
        ("icu_bed_occupied", 11, int),
        ("icu_bed_vacant", 12, int),
        ("last_updated_date", 16, str),
        ("last_updated_time", 17, str),
    ]

    govt_dict: t_FullDict = {"district": []}
    for k, _, _ in key_colid_dtype:
        govt_dict[k] = []

    table = govt_soup.find("table")
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
        govt_dict["district"].append(current_district)
        for k, kid, dtype in key_colid_dtype:
            govt_dict[k].append(dtype(cells[kid + offset].string.strip()))

    logging.info("..done")
    return govt_dict


def parse_private_hospitals(private_soup: t_BeautifulSoup) -> t_FullDict:
    logging.info("parsing hospitals page..")
    private_dict = parse_government_hospitals(private_soup)
    logging.info("..done")
    return private_dict
