from collections import defaultdict

import pandas as pd

from typing import Dict, Tuple, Optional

from hydbedscraper.types import t_TableList, t_Table

col_id_of_serial_number = 0
invalid_category_strings = ["Status of vacancy of Private beds", "O = Occupied"]
unknown_category_tag = "UNKNOWN_HOSPITAL_CATEGORY"

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


def _find_category_name(
    table: t_Table, search_start_row: int, current_hospital_category: Optional[str]
) -> str:
    # go backwards up the rows
    for row_index in range(search_start_row, -1, -1):
        row = table.df.iloc[row_index, :]
        # ensure previous row is category row by making sure all other columns are empty
        all_columns_except_first_column_are_empty = pd.DataFrame.all(row[1:] == "")
        if all_columns_except_first_column_are_empty:
            category_candidate = row[0]
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
                continue
        else:
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
    hospital_category_to_information_dict = defaultdict(lambda: defaultdict(list))
    # read date and time

    # current hospital-category
    current_hospital_category = None

    for table in hospital_tables:
        category_to_start_end_index_tuple_map = (
            _get_hospital_category_information_for_table(
                table, current_hospital_category
            )
        )

        for category, (
            start_index,
            end_index,
        ) in category_to_start_end_index_tuple_map.items():
            for row_index in range(start_index, end_index + 1):
                for key, col_id, dtype in key_colid_dtype:
                    hospital_category_to_information_dict[category][key].append(
                        table.df.iloc[row_index, col_id]
                    )
            current_hospital_category = category

        # first column is serial number
        # when serial number is 1, check previous row for type and ensure all other columns of that row are ""

    # second column is zone / ward. Split by "/" - first part is zone, second part is ward

    # third column is hospital name. Replace "\n" with " "

    # If table has no serial number column, it is Dedicated COVID Health Center (DCHC)

    return hospital_category_to_information_dict
