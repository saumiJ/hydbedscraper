import json
import logging
import pandas

from hydbedscraper.parsers import (
    parse_summary,
    parse_government_hospitals,
    parse_private_hospitals,
)
from hydbedscraper.requests import (
    get_summary_page_soup,
    get_government_hospitals_page_soup,
    get_private_hospitals_page_soup,
)


# TODO: setup proper logging
logging.getLogger().setLevel(logging.INFO)


def work():
    # TODO: performance optimization
    # TODO: tests
    summary_soup = get_summary_page_soup(use_test=False)
    govt_soup = get_government_hospitals_page_soup(use_test=False)
    private_soup = get_private_hospitals_page_soup(use_test=False)

    summary = parse_summary(summary_soup)
    govt_info = parse_government_hospitals(govt_soup)
    private_info = parse_private_hospitals(private_soup)

    logging.info("dumping data..")
    with open("summary.json", "w") as fp:
        json.dump(summary, fp, indent=2)
    govt_df = pandas.DataFrame.from_dict(govt_info)
    private_df = pandas.DataFrame.from_dict(private_info)
    govt_df.to_csv("govt.csv")
    private_df.to_csv("private.csv")
    logging.info(".. done.")


if __name__ == "__main__":
    work()
