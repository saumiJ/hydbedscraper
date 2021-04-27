import pandas as pd

from typing import Dict

from hydbedscraper.types import t_DataFrameDict

ICU_VENTILATOR_BED_DATAFRAME_KEY = "icu_ventilator_bed_info"
ICU_NON_VENTILATOR_BED_DATAFRAME_KEY = "icu_non_ventilator_bed_info"
OXYGEN_BED_DATAFRAME_KEY = "oxygen_bed_info"
NORMAL_BED_DATAFRAME_KEY = "normal_bed_info"


def to_dataframe_dict(
    icu_ventilator_bed_info: Dict,
    icu_non_ventilator_bed_info: Dict,
    oxygen_bed_info: Dict,
    normal_bed_info: Dict,
) -> t_DataFrameDict:
    return {
        ICU_VENTILATOR_BED_DATAFRAME_KEY: pd.DataFrame.from_dict(
            icu_ventilator_bed_info
        ),
        ICU_NON_VENTILATOR_BED_DATAFRAME_KEY: pd.DataFrame.from_dict(
            icu_non_ventilator_bed_info
        ),
        OXYGEN_BED_DATAFRAME_KEY: pd.DataFrame.from_dict(oxygen_bed_info),
        NORMAL_BED_DATAFRAME_KEY: pd.DataFrame.from_dict(normal_bed_info),
    }
