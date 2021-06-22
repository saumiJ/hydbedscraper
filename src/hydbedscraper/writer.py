import pandas as pd

from typing import Dict

from hydbedscraper.parsers.helpers.labels import Label
from hydbedscraper.types import t_DataFrame


def to_dataframe(info_dict: Dict[Label, list]) -> t_DataFrame:
    info_str_labels_dict = {k.value: v for k, v in info_dict.items()}
    return pd.DataFrame.from_dict(info_str_labels_dict)
