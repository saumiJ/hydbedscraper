import pandas as pd
import re

from collections import defaultdict
from typing import Dict, Tuple, Optional

from hydbedscraper.parsers._cleaners import dtype_to_cleaner_map
from hydbedscraper.types import t_TableList, t_Table

col_id_of_serial_number = 0
invalid_category_strings = ["Status of vacancy of Private beds", "O = Occupied"]
unknown_category_tag = "UNKNOWN_HOSPITAL_CATEGORY"
dchc_category_tag = "DCHC"
dchc_first_cell_label = "TOTAL DCHC"
dchc_index_offset = -2

key_colid_dtype = [
    ("hospital_name", 2, str),
    ("isolation_occupied", 3, int),
    ("isolation_vacant", 4, int),
    ("hdu_occupied", 5, int),
    ("hdu_vacant", 6, int),
    ("icu_no_ventilator_occupied", 7, int),
    ("icu_no_ventilator_vacant", 8, int),
    ("icu_ventilator_occupied", 9, int),
    ("icu_ventilator_vacant", 10, int),
]
date_key = "date"
time_key = "time"


def _get_date_and_time(table_list: t_TableList) -> Tuple[str, str]:
    # ASSMUPTION: Date and time are stored in first column of some row
    for table in table_list:
        date_time_regex = r".*Date: *(.*) *Time: *(.*)"
        for cell in table.df[0]:
            regex_result = re.search(date_time_regex, cell)
            if regex_result:
                date_str = regex_result.group(1)
                time_str = regex_result.group(2)
                return date_str, time_str
    return "??/??/????", "??:?? ??"


def _find_category_name(
    table: t_Table, search_start_row: int, current_hospital_category: Optional[str]
) -> str:
    # go backwards up the rows
    for row_index in range(search_start_row, -1, -1):
        row = table.df.iloc[row_index, :]
        # ASSUMPTION: row with category information contains only one occupied cell
        all_columns_except_first_column_are_empty = pd.DataFrame.all(row[1:] == "")
        if all_columns_except_first_column_are_empty:
            category_candidate = row[0]
            # filter out invalid candidates
            valid = True
            for invalid_category_string in invalid_category_strings:
                if invalid_category_string in category_candidate:
                    valid = False
                    break
            if valid:
                return category_candidate
            else:
                continue
        else:
            # continue trying earlier rows
            continue
    # if not found, check if current category exists
    if current_hospital_category is not None:
        return current_hospital_category
    else:
        return unknown_category_tag


def _get_hospital_category_information_for_table(
    table: t_Table, current_hospital_category: Optional[str]
) -> Dict[str, Tuple[int, int]]:
    category_to_start_end_index_tuple_map = dict()
    active_category = None
    start_index = None
    for row_index, val in enumerate(table.df[col_id_of_serial_number]):
        try:
            # see if row has serial number
            # ASSUMPTION: serial number can be converted to integer
            int(val)
        except ValueError:
            # cannot convert to integer
            if start_index is not None:
                # we have come to the end of a category
                # store end index and prepare for next block
                assert start_index is not None
                assert active_category is not None
                end_index = row_index - 1
                category_to_start_end_index_tuple_map[active_category] = (
                    start_index,
                    end_index,
                )
                start_index = None
                active_category = None
            else:
                # no category block has begun yet, and no serial number row has been found yet
                # continue looping through rows
                continue
        else:
            # the row begins with a serial number - therefore it has data
            if row_index == 0:
                # the first row already starts with data
                # assume category is active from earlier table
                assert start_index is None
                assert current_hospital_category is not None
                active_category = current_hospital_category
                start_index = row_index
            elif row_index == table.df.shape[0] - 1:
                # end of page, table continues into the next page
                assert start_index is not None
                assert active_category is not None
                end_index = row_index
                category_to_start_end_index_tuple_map[active_category] = (
                    start_index,
                    end_index,
                )
                start_index = None
                active_category = None
            elif active_category is None:
                # we just found a new category!
                active_category = _find_category_name(
                    table, row_index - 1, current_hospital_category
                )
                start_index = row_index
            else:
                # nothing to do, we are still going through a block
                continue
    return category_to_start_end_index_tuple_map


def parse_hospital_tables(hospital_tables: t_TableList) -> Dict[str, Dict[str, list]]:
    hospital_category_to_information_dict: Dict[str, Dict[str, list]] = defaultdict(
        lambda: defaultdict(list)
    )
    # read date and time
    date_str, time_str = _get_date_and_time(hospital_tables)

    # current hospital-category
    current_hospital_category = None

    for table in hospital_tables:
        # get map from hospital-category to start and end row-index of that category
        category_to_start_end_index_tuple_map = (
            _get_hospital_category_information_for_table(
                table, current_hospital_category
            )
        )

        # go over each hospital-category
        for category, (
            start_index,
            end_index,
        ) in category_to_start_end_index_tuple_map.items():
            # go over each row for that category
            for row_index in range(start_index, end_index + 1):
                # go over each information-cell
                for key, col_id, dtype in key_colid_dtype:
                    # add information
                    raw = table.df.iloc[row_index, col_id]
                    cleaned = dtype_to_cleaner_map[dtype](raw)
                    hospital_category_to_information_dict[category][key].append(
                        cleaned
                    )
                # add date and time information
                hospital_category_to_information_dict[category][date_key].append(date_str)
                hospital_category_to_information_dict[category][time_key].append(time_str)
            # store current hospital category
            current_hospital_category = category

        if len(category_to_start_end_index_tuple_map.keys()) == 0:
            # ASSUMPTION: Dedicated COVID Health Center (DCHC) table has no serial number information
            # Detect it with the label of its summary row
            for row_index in range(table.shape[0]):
                first_cell = table.df[0][row_index]
                if isinstance(first_cell, str):
                    if dchc_first_cell_label in first_cell:
                        for key, col_id, dtype in key_colid_dtype:
                            # add information
                            raw = table.df.iloc[row_index, col_id + dchc_index_offset]
                            cleaned = dtype_to_cleaner_map[dtype](raw)
                            hospital_category_to_information_dict[dchc_category_tag][key].append(
                                cleaned
                            )
                        # add date and time information
                        hospital_category_to_information_dict[dchc_category_tag][date_key].append(date_str)
                        hospital_category_to_information_dict[dchc_category_tag][time_key].append(time_str)

    return hospital_category_to_information_dict
