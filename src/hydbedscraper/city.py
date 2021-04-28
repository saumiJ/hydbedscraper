import logging
from enum import Enum

from hydbedscraper.drivers import hyderabad, ahmedabad, vadodara


class City(Enum):
    AHMEDABAD = "ahmedabad"
    HYDERABAD = "hyderabad"
    VADODARA = "vadodara"

    def work(self):
        logging.info(f"working at {self.value}")
        if self is City.AHMEDABAD:
            return ahmedabad.work()
        elif self is City.HYDERABAD:
            return hyderabad.work()
        elif self is City.VADODARA:
            return vadodara.work()
        else:
            raise NotImplementedError(self)


def get_city_from_str(city_name: str) -> City:
    try:
        return City(city_name)
    except ValueError as exc:
        raise ValueError(f"Supported cities: {[city.value for city in City]}") from exc
