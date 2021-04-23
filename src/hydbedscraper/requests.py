import logging
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from hydbedscraper.testdata.path import (
    test_summary_html,
    test_government_hospital_data_html,
    test_private_hospital_data_html,
)
from hydbedscraper.types import t_BeautifulSoup, t_Response

base_URL = "http://164.100.112.24/SpringMVC/"


def _decode_streamed_response(response: t_Response) -> str:
    response_content = ""
    for chunk in response.iter_content(8192, decode_unicode=True):
        response_content += chunk
    return response_content


def get_summary_page_soup(use_test: bool = True) -> t_BeautifulSoup:
    logging.info("getting summary page..")
    if use_test:
        with open(test_summary_html, "r") as fp:
            soup = BeautifulSoup(fp, "lxml")
    else:
        page = requests.get(
            urljoin(base_URL, "Hospital_Beds_Statistic_Bulletin_citizen.htm"),
            stream=True,
        )
        soup = BeautifulSoup(_decode_streamed_response(page), "lxml")
    logging.info("..done")
    return soup


def get_government_hospitals_page_soup(use_test: bool = True) -> t_BeautifulSoup:
    logging.info("getting government hospitals page..")
    if use_test:
        with open(test_government_hospital_data_html, "r") as fp:
            soup = BeautifulSoup(fp, "lxml")
    else:
        page = requests.post(
            urljoin(base_URL, "getHospital_Beds_Status_Citizen.htm"),
            data={
                "hospital": "G",
            },
            stream=True,
        )
        soup = BeautifulSoup(_decode_streamed_response(page), "lxml")
    logging.info("..done")
    return soup


def get_private_hospitals_page_soup(use_test: bool = True) -> t_BeautifulSoup:
    logging.info("getting private hospitals page..")
    if use_test:
        with open(test_private_hospital_data_html, "r") as fp:
            soup = BeautifulSoup(fp, "lxml")
    else:
        page = requests.post(
            urljoin(base_URL, "getHospital_Beds_Status_Citizen.htm"),
            data={
                "hospital": "P",
            },
            stream=True,
        )
        soup = BeautifulSoup(_decode_streamed_response(page), "lxml")
    logging.info("..done")
    return soup
