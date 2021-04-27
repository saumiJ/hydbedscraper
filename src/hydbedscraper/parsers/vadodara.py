from collections import defaultdict
from typing import Dict, List, Tuple

from hydbedscraper.types import t_BeautifulSoup


def _get_key_colid_type(bed_soup: t_BeautifulSoup) -> List[Tuple[str, int, type]]:
    _type: type
    key_colid_type: List[Tuple[str, int, type]] = list()
    rows = bed_soup("tr")
    for row in rows:
        cells = row("th")
        if len(cells) > 0:
            for col_id, cell in enumerate(cells):
                value = cell.string.strip()
                if value.lower() in ["total", "occupied", "vacant"]:
                    _type = int
                else:
                    _type = str
                key_colid_type.append((value, col_id, _type))
            return key_colid_type
    raise ValueError(f"could not locate header information, \nraw data: {bed_soup}")


def parse_bed_soup(bed_soup: t_BeautifulSoup) -> Dict:
    key_colid_type = _get_key_colid_type(bed_soup)
    num_columns = len(key_colid_type)
    info_dict = defaultdict(list)

    rows = bed_soup("tr")
    for row in rows:
        cells = row("td")
        if len(cells) != num_columns:
            continue
        for key, col_id, _type in key_colid_type:
            info_dict[key].append(_type(cells[col_id].string))

    return info_dict
