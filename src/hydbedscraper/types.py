from bs4 import BeautifulSoup, Tag
from requests.models import Response
from typing import Dict, List

t_BeautifulSoup = BeautifulSoup
t_Tag = Tag

t_Response = Response

t_SummaryDict = Dict[str, Dict[str, Dict[str, int]]]
t_FullDict = Dict[str, List]
