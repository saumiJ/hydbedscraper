import json

from hydbedscraper.parsers import parse_summary
from hydbedscraper.requests import get_summary_page_soup, get_government_hospitals_page_soup


def main():
    base_soup = get_summary_page_soup(use_test=False)
    get_government_hospitals_page_soup()
    summary = parse_summary(base_soup)
    with open("summary.json", "w") as fp:
        json.dump(summary, fp, indent=2)


if __name__ == "__main__":
    main()
