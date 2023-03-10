"""Analyse TM1 transaction log files"""

__version__ = "0.1"

import csv

from visidata import (  # ColumnAttr,; options,
    Column,
    ItemColumn,
    TableSheet,
    TypedExceptionWrapper,
    VisiData,
    date,
    stacktrace,
    vd,
)

# options for filtering the results
vd.option("tm1_cube", "", "include only specific cube (implies tm1_ctrl)", replay=True)
vd.option("tm1_ctrl", False, "include control cubes", replay=True)
vd.option("tm1_user", "", "include only specific user", replay=True)
vd.option("tm1_dt", "", "include only specific datatype (N or S)", replay=True)
vd.option("tm1_deltas", True, "include delta columns for numeric values", replay=True)


@VisiData.api
def open_tm1log(vd, p):
    return TM1LogSheet(p.name, source=p)


def remove_metadata_lines(fp):

    # there are metadata lines in the file that we want to skip
    # all such lines start with a #, sometimes with a leading space
    # there's a trailing with a single weird char (this can be handled more elegantly surely)

    for line in fp:

        if line[0] == "#" or len(line) < 3 or line[1] == "#":
            continue
        else:
            yield line


class TM1LogSheet(TableSheet):

    rowtype = "cube changes"  # rowdef: list

    non_el_columns = 9

    def __init__(self, name, source, tm1_ctrl=None, tm1_cube=None, tm1_user=None, tm1_dt=None, tm1_deltas=None):

        super().__init__(name=name, source=source)

        self.tm1_cube = vd.options.tm1_cube.lower() if tm1_cube is None else tm1_cube
        # filtering for a specific cube implies show control
        if self.tm1_cube:
            self.tm1_ctrl = True
        else:
            self.tm1_ctrl = vd.options.tm1_ctrl if tm1_ctrl is None else tm1_ctrl
        self.tm1_user = vd.options.tm1_user.lower() if tm1_user is None else tm1_user
        self.tm1_dt = vd.options.tm1_dt.lower() if tm1_dt is None else tm1_dt
        self.tm1_deltas = vd.options.tm1_deltas if tm1_deltas is None else tm1_deltas

    # create fixed columns

    columns = [
        Column("Time", type=date, fmtstr="%Y-%m-%d %H:%M:%S", getter=lambda col, row: row[1]),
        ItemColumn("Cube", 7),
        ItemColumn("User", 3),
        ItemColumn("T", 4),
        # # we'll always have at least two elements in a cube
        Column("El Cnt", type=int, getter=lambda col, row: len(row) - 8),
        ItemColumn("El 1", 8),
        ItemColumn("El 2", 9),
        # set these to hidden and unhide when a non null value received somehow
        Column("Old Val N", width=0, type=float, getter=lambda col, row: row[5] if row[4] == "N" else None),
        Column("New Val N", width=0, type=float, getter=lambda col, row: row[6] if row[4] == "N" else None),
        Column(
            "Delta",
            width=0,
            type=float,
            getter=lambda col, row: (float(row[6]) - float(row[5])) if row[4] == "N" else None,
        ),
        Column(
            "Abs Delta",
            width=0,
            type=float,
            getter=lambda col, row: abs(float(row[6]) - float(row[5])) if row[4] == "N" else None,
        ),
        Column("Old Val S", width=0, type=str, getter=lambda col, row: row[5] if row[4] == "S" else None),
        Column("New Val S", width=0, type=str, getter=lambda col, row: row[6] if row[4] == "S" else None),
    ]

    def iterload(self):

        with self.source.open_text(encoding=self.options.encoding) as fp:

            # the log lines are comma delimited and double quoted
            rdr = csv.reader(remove_metadata_lines(fp))

            el_count = 2

            has_n = False
            has_s = False

            # not sure this is the best place to do this but it works
            self.setKeys(self.columns[0:3])

            while True:
                try:

                    row = next(rdr)

                    # each log row seems to contain an empty string at the end
                    row = row[:-1]

                    # filter for specific cube if asked to
                    cube = row[7]

                    if self.tm1_cube and cube.lower() != self.tm1_cube:

                        continue

                    # only include ctrl cubes if requested
                    if not self.tm1_ctrl and cube[0] == "}":

                        continue

                    # filter for specific user if asked to
                    user = row[3]

                    if self.tm1_user and user.lower() != self.tm1_user:

                        continue

                    # filter just for strings or numbers
                    datatype = row[4]

                    if self.tm1_dt and datatype.lower() != self.tm1_dt:

                        continue

                    # I think each log line has a trailing empty string for some reason
                    # row = row[:-1]

                    row_el_cols = len(row) - 8

                    while el_count < row_el_cols:

                        # we need to add all new columns

                        el_count = el_count + 1

                        col = ItemColumn(f"El {el_count}", el_count + 7)

                        col_index = el_count + 4

                        self.addColumn(col, index=col_index)

                    # unhide value columns once type hit

                    if not has_n and datatype == "N":
                        self.columns[-6].width = 8
                        self.columns[-5].width = 8
                        if self.tm1_deltas:
                            self.columns[-4].width = 8
                            self.columns[-3].width = 8

                    if not has_s and datatype == "S":
                        self.columns[-2].width = 8
                        self.columns[-1].width = 8

                    # do I need to do anything here to add new columns?
                    yield row

                except csv.Error as e:
                    e.stacktrace = stacktrace()
                    yield [TypedExceptionWrapper(None, exception=e)]
                except StopIteration:
                    return


vd.addGlobals({"TM1LogSheet": TM1LogSheet})
