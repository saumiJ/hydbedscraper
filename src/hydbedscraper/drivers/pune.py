from hydbedscraper.parsers.pune import parse_bed_soups
from hydbedscraper.requesters.pune import get_bed_soups
from hydbedscraper.types import t_DataFrameDict
from hydbedscraper.writers.pune import to_dataframe_dict


def work() -> t_DataFrameDict:
    bed_soups = get_bed_soups()
    bed_info = parse_bed_soups(bed_soups)
    return to_dataframe_dict(bed_info)


if __name__ == "__main__":
    print(work())
