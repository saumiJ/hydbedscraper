import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from hydbedscraper.testdata.path import test_summary_html, test_government_hospital_data_html
from hydbedscraper.type import t_BeautifulSoup


base_URL = "http://164.100.112.24/SpringMVC/"


def get_summary_page_soup(use_test: bool = True) -> t_BeautifulSoup:
    if use_test:
        with open(test_summary_html, "r") as fp:
            soup = BeautifulSoup(fp, "lxml")
    else:
        page = requests.get(
            urljoin(base_URL, "Hospital_Beds_Statistic_Bulletin_citizen.htm"),
            stream=True,
        )
        response_content = ""
        for chunk in page.iter_content(8192, decode_unicode=True):
            response_content += chunk
        soup = BeautifulSoup(response_content, "lxml")
    return soup


def get_government_hospitals_page_soup(use_test: bool = True) -> t_BeautifulSoup:
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
        response_content = ""
        for chunk in page.iter_content(8192, decode_unicode=True):
            response_content += chunk
        soup = BeautifulSoup(response_content, "lxml")
    return soup
