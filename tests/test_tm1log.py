# import csv

import pytest

from plugins.vd_tm1log import TM1LogSheet  # , remove_metadata_lines


@pytest.fixture
def tm1log_test_sheet():

    # open the sample.log and return the file

    # not sure this is getting actual file
    source = "sample_small.log"

    sheet: TM1LogSheet = TM1LogSheet(source=source, name="test_tm1log_sheet")

    return sheet


def test_fixed_cols(tm1log_test_sheet):

    # basic check on fixed cols
    assert tm1log_test_sheet
    assert len(tm1log_test_sheet.columns) > 0
    assert tm1log_test_sheet.columns[0].name == "Time"
    assert tm1log_test_sheet.columns[1].name == "Cube"
    assert tm1log_test_sheet.columns[2].name == "User"

    assert tm1log_test_sheet.columns[5].name == "El 1"
    assert tm1log_test_sheet.columns[6].name == "El 2"


@pytest.mark.skip("Not yet implemented")
def test_remove_metadata():

    pass


@pytest.mark.skip("Test broken")
def test_rows(tm1log_test_sheet):

    # check we have at least a couple of rows

    assert len(tm1log_test_sheet.rows) == 0

    # naively I'm hoping this will load the test rows
    tm1log_test_sheet.iterload()

    assert len(tm1log_test_sheet.rows) != 0
