import pandas as pd

from hydbedscraper.types import t_FullDict, t_DataFrameDict

GOVT_DATAFRAME_KEY = "hyderabad_government_info"
PRIVATE_DATAFRAME_KEY = "hyderabad_private_info"


def to_dataframe_dict(
    govt_info: t_FullDict, private_info: t_FullDict
) -> t_DataFrameDict:
    return {
        GOVT_DATAFRAME_KEY: pd.DataFrame.from_dict(govt_info),
        PRIVATE_DATAFRAME_KEY: pd.DataFrame.from_dict(private_info),
    }
