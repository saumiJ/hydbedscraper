import pandas as pd

from typing import Dict

from hydbedscraper.types import t_DataFrameDict


def to_dataframe_dict(
    bed_info: Dict,
) -> t_DataFrameDict:
    return {"BED_INFO": pd.DataFrame.from_dict(bed_info)}
