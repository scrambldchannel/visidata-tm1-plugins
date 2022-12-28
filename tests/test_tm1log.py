# import csv

import pytest

from plugins.vd_tm1log import remove_metadata_lines  # noqa

from .common import load_vd_sheet

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


def test_rows(sample_log_sheet):

    assert sample_log_sheet

    assert len(sample_log_sheet.rows) > 0

    assert len(sample_log_sheet.rows) == 16
