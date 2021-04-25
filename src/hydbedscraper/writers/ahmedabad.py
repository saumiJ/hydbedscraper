import pandas as pd

from typing import Dict


def to_dataframe_dict(
    hospital_category_to_information_dict: Dict[str, Dict[str, list]]
):
    return {
        hospital_category: pd.DataFrame.from_dict(information)
        for hospital_category, information in hospital_category_to_information_dict.items()
    }
