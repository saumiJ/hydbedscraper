from typing import Callable, Dict


def clean_int(raw: str) -> int:
    newline_separations = raw.split("\n")
    for substr in newline_separations:
        try:
            int(substr)
        except ValueError:
            continue
        else:
            return int(substr)
    raise TypeError(f"could not clean {raw} for integer")


def clean_str(raw: str) -> str:
    return raw


dtype_to_cleaner_map: Dict[type, Callable] = {int: clean_int, str: clean_str}
