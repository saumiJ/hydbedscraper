# contains absolute paths to testdata-files from project root

from pathlib import Path

_test_dir = Path(__file__).parent.absolute()

test_summary_html = _test_dir.joinpath("summary.html")
test_government_hospital_data_html = _test_dir.joinpath("government_hospitals_data.html")
