import bs4
import camelot
import pandas
import requests

from typing import Dict

# bs4
t_BeautifulSoup = bs4.BeautifulSoup
t_Tag = bs4.Tag

# response
t_Response = requests.models.Response

# pandas
t_DataFrame = pandas.DataFrame
t_DataFrameDict = Dict[str, pandas.DataFrame]

# camelot
t_Table = camelot.core.Table
t_TableList = camelot.core.TableList
