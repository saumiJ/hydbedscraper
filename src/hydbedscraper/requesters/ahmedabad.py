import camelot
import logging
import re

from urllib.parse import urljoin

import requests
from hydbedscraper.requesters._common import decode_streamed_string_response
from hydbedscraper.types import t_TableList

base_URL = "https://ahna.org.in/"


def get_hospital_tables() -> t_TableList:
    logging.info("getting hospital tables..")

    def _get_hospitals_pdf_url_suffix() -> str:
        hospitals_pdf_prefix = "AMC REQUISITIONED HOSPITAL STATUS"
        hospitals_pdf_suffix = "pdf"
        hospitals_pdf_regex_pattern = (
            fr"{hospitals_pdf_prefix}.*\.{hospitals_pdf_suffix}"
        )

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

    # get pdf-url suffix
    pdf_url_suffix = _get_hospitals_pdf_url_suffix()

    # ask camelot to read pdf at url
    tables = camelot.read_pdf(
        urljoin(base_URL, pdf_url_suffix),
        pages="all",
        line_scale=40,  # necessary to detect smaller tables
    )

    logging.info("..done")
    return tables
