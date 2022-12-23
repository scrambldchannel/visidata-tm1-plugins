import csv

from visidata import (  # ColumnAttr,; options,
    Column,
    ItemColumn,
    TableSheet,
    TypedExceptionWrapper,
    VisiData,
    stacktrace,
    vd,
)


@VisiData.api
def open_tm1log(vd, p):
    return TM1LogSheet(p.name, source=p)


def remove_metadata_lines(fp):

    # there are metadata lines in the file that we want to skip
    # all such lines start with a #, sometimes with a leading space
    # there's a trailing with a single weird char (this can be handled more elegantly surely)
    for line in fp:

        if line[0] == "#" or len(line) == 1 or line[1] == "#":
            continue
        else:
            yield line


class TM1LogSheet(TableSheet):

    rowtype = "changes"  # rowdef: list

    # create fixed columns

    columns = [
        # worry about formatting later
        ItemColumn("Time", 1),
        ItemColumn("Cube", 7),
        ItemColumn("User", 3),
        ItemColumn("T", 4),
        Column("Old Val N", getter=lambda col, row: row[5] if row[4] == "N" else None),
        Column("New Val N", getter=lambda col, row: row[6] if row[4] == "N" else None),
        Column("Old Val S", getter=lambda col, row: row[5] if row[4] == "S" else None),
        Column("New Val S", getter=lambda col, row: row[6] if row[4] == "S" else None),
        # # we'll always have at least two elements in a cube
        ItemColumn("El 1", 8),
        ItemColumn("El 2", 9),
    ]

    def iterload(self):

        with self.source.open_text(encoding=self.options.encoding) as fp:

            # the log lines are comma delimited and double quoted
            rdr = csv.reader(remove_metadata_lines(fp))

            while True:
                try:

                    row = next(rdr)

                    # do I need to do anything here to add new columns?
                    yield row

                except csv.Error as e:
                    e.stacktrace = stacktrace()
                    yield [TypedExceptionWrapper(None, exception=e)]
                except StopIteration:
                    return


# not sure where this should be done / or whether there's a better way to achieve this
TM1LogSheet.class_options.header = 0

vd.addGlobals({"TM1LogSheet": TM1LogSheet})
