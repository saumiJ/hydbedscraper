from hydbedscraper.types import t_BeautifulSoup, t_SummaryDict, t_FullDict


def parse_summary(summary_soup: t_BeautifulSoup) -> t_SummaryDict:
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
    summary_table = summary_soup.find("table")

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


def parse_government_hospitals(govt_soup: t_BeautifulSoup) -> t_FullDict:
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

    return govt_dict


def parse_private_hospitals(private_soup: t_BeautifulSoup) -> t_FullDict:
    return parse_government_hospitals(private_soup)
