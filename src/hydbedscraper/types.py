from bs4 import BeautifulSoup, Tag
from pandas import DataFrame
from requests.models import Response
from typing import Dict, List

t_BeautifulSoup = BeautifulSoup
t_Tag = Tag

t_Response = Response

t_DataFrame = DataFrame

t_SummaryDict = Dict[str, Dict[str, Dict[str, int]]]
t_FullDict = Dict[str, List]
t_DataFrameDict = Dict[str, DataFrame]
