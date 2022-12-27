# import csv

import pytest

from .common import load_vd_sheet

# from plugins.vd_tm1log import TM1LogSheet  # , remove_metadata_lines


SAMPLE_FILE = "tests/sample_log.log"


@pytest.fixture(scope="function")
def sample_log_sheet():
    return load_vd_sheet(SAMPLE_FILE, filetype="tm1log")


def test_cols(sample_log_sheet):

    assert sample_log_sheet

    # we should have all the fixed columns at least
    assert len(sample_log_sheet.columns) >= 13

    assert sample_log_sheet.columns[0].name == "Time"
    assert sample_log_sheet.columns[1].name == "Cube"

    assert sample_log_sheet.columns[2].name == "User"
    assert sample_log_sheet.columns[3].name == "T"
    assert sample_log_sheet.columns[4].name == "El Cnt"
    assert sample_log_sheet.columns[5].name == "El 1"
    assert sample_log_sheet.columns[6].name == "El 2"

    assert sample_log_sheet.columns[-6].name == "Old Val N"
    assert sample_log_sheet.columns[-5].name == "New Val N"
    assert sample_log_sheet.columns[-4].name == "Delta"
    assert sample_log_sheet.columns[-3].name == "Abs Delta"

    assert sample_log_sheet.columns[-2].name == "Old Val S"
    assert sample_log_sheet.columns[-1].name == "New Val S"


def test_rows(sample_log_sheet):

    assert sample_log_sheet

    assert len(sample_log_sheet.rows) > 0

    assert len(sample_log_sheet.rows) == 16
