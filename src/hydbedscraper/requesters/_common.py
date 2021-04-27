import requests

from bs4 import BeautifulSoup
from typing import Optional

from hydbedscraper.types import t_Response, t_BeautifulSoup


def decode_streamed_string_response(response: t_Response) -> str:
    response_content = ""
    for chunk in response.iter_content(8192, decode_unicode=True):
        response_content += chunk
    return response_content


def soupify_page(
    url: str,
    params: Optional[dict] = None,
    data: Optional[dict] = None,
    stream: bool = True,
) -> t_BeautifulSoup:
    page = requests.post(
        url,
        params=params,
        data=data,
        stream=stream,
    )
    return BeautifulSoup(decode_streamed_string_response(page), "lxml")
