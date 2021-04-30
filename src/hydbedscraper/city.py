import logging
from enum import Enum

from hydbedscraper.drivers import hyderabad, ahmedabad, vadodara, pune


class City(Enum):
    AHMEDABAD = "ahmedabad"
    HYDERABAD = "hyderabad"
    PUNE = "pune"
    VADODARA = "vadodara"

    def work(self):
        logging.info(f"working at {self.value}")
        work_method_dict = {
            City.AHMEDABAD: ahmedabad.work,
            City.HYDERABAD: hyderabad.work,
            City.PUNE: pune.work,
            City.VADODARA: vadodara.work,
        }
        try:
            return work_method_dict[self]()
        except KeyError:
            raise NotImplementedError(self)


def get_city_from_str(city_name: str) -> City:
    try:
        return City(city_name)
    except ValueError as exc:
        raise ValueError(f"Supported cities: {[city.value for city in City]}") from exc
