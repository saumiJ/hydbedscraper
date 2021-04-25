import logging

from hydbedscraper.city import get_city_from_str
from hydbedscraper.types import t_DataFrameDict


# TODO: setup proper logging
logging.getLogger().setLevel(logging.INFO)


def work(city_name: str) -> t_DataFrameDict:
    """
    :param city_name: lowercase name of city whose hospital-bed-availability info is required
    :return: string-to-DataFrame map
    """
    city = get_city_from_str(city_name)
    return city.work()
