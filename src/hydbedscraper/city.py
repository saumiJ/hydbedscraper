from enum import Enum

from hydbedscraper.drivers import hyderabad, amdavad


class City(Enum):
    AMDAVAD = "amdavad"
    HYDERABAD = "hyderabad"

    def work(self):
        if self is City.HYDERABAD:
            return hyderabad.work()
        elif self is City.AMDAVAD:
            return amdavad.work()
        else:
            raise NotImplementedError(self)


def get_city_from_str(city_name: str) -> City:
    try:
        return City(city_name)
    except ValueError as exc:
        raise ValueError(f"Supported cities: {[city for city in City]}") from exc
