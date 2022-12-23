import csv

from plugins.vd_tm1log import TM1LogRow, remove_metadata_lines

# import pytest


sample_file = "tests/sample.log"


def test_remove_metadata_lines():

    with open(sample_file) as fp:

        reader = csv.reader(remove_metadata_lines(fp))

        row = next(reader)

        assert row

        tm1log_row = TM1LogRow(row)

        assert tm1log_row.user == "Admin"
        assert tm1log_row.type == "S"
