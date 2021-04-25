import re
import camelot

from urllib.parse import urljoin

import requests
from hydbedscraper.requesters.common import decode_streamed_string_response
from hydbedscraper.types import t_TableList

base_URL = "https://ahna.org.in/"

local_pdf_document_name = "amdavad_source.pdf"


def _get_hospitals_pdf_url_suffix() -> str:
    hospitals_pdf_prefix = "AMC REQUISITIONED HOSPITAL STATUS"
    hospitals_pdf_suffix = "pdf"
    hospitals_pdf_regex_pattern = fr'{hospitals_pdf_prefix}.*\.{hospitals_pdf_suffix}'

    # get page
    page = requests.post(
        urljoin(base_URL, "covid19.html"),
        stream=True,
    )
    response_content = decode_streamed_string_response(page)

    # find pdf name in page content
    match_object = re.search(hospitals_pdf_regex_pattern, response_content)
    if match_object:
        pdf_name = match_object.group(0)
    else:
        raise ValueError("could not determine pdf name")

    # replace spaces
    pdf_url = pdf_name.replace(" ", "%20")
    return pdf_url


def _get_hospital_tables() -> t_TableList:
    # get pdf-url suffix
    pdf_url_suffix = _get_hospitals_pdf_url_suffix()

    # ask camelot to read pdf at url
    tables = camelot.read_pdf(
        urljoin(base_URL, pdf_url_suffix),
        pages="all",
    )

    return tables


if __name__ == '__main__':
    _get_hospital_tables()
