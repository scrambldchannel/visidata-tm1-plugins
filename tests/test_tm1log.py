# import csv

import pytest

from .common import load_vd_sheet

# from plugins.vd_tm1log import TM1LogSheet  # , remove_metadata_lines


SAMPLE_FILE = "tests/sample_log.log"


@pytest.fixture(scope="function")
def sample_log_sheet():
    return load_vd_sheet(SAMPLE_FILE, filetype="tm1log")


def test_sheet_basics(sample_log_sheet):

    assert sample_log_sheet

    print(type(sample_log_sheet))

    # we should have all the fixed columns at least
    assert len(sample_log_sheet.columns) >= 13
    # we should have some rows
    assert len(sample_log_sheet.rows) > 0

    assert sample_log_sheet.columns[0].name == "Time"
    assert sample_log_sheet.columns[1].name == "Cube"
