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
vd.option("tm1_ctrl", False, "include control cubes", replay=True)
vd.option("tm1_cube", "", "include only specific cube", replay=True)
vd.option("tm1_user", "", "include only specific user", replay=True)
# hacking the date format, not sure this the best place...
vd.option("disp_date_fmt", "%Y-%m-%d %H:%M:%S", "default fmtstr to strftime for date values", replay=True)


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

    rowtype = "changes"  # rowdef: list

    non_el_columns = 9

    def __init__(self, name, source, tm1_ctrl=None, tm1_cube=None, tm1_user=None):

        super().__init__(name=name, source=source)

        self.tm1_ctrl = vd.options.tm1_ctrl if tm1_ctrl is None else tm1_ctrl
        self.tm1_cube = vd.options.tm1_cube if tm1_cube is None else tm1_cube
        self.tm1_user = vd.options.tm1_user if tm1_user is None else tm1_user

    # create fixed columns

    columns = [
        Column("Time", width=18, type=date, getter=lambda col, row: row[1]),
        ItemColumn("Cube", 7),
        ItemColumn("User", 3),
        ItemColumn("T", 4),
        # set these to hidden and unhide when a non null value received somehow
        Column("Old Val N", width=0, type=float, getter=lambda col, row: row[5] if row[4] == "N" else None),
        Column("New Val N", width=0, type=float, getter=lambda col, row: row[6] if row[4] == "N" else None),
        Column("Old Val S", width=0, type=str, getter=lambda col, row: row[5] if row[4] == "S" else None),
        Column("New Val S", width=0, type=str, getter=lambda col, row: row[6] if row[4] == "S" else None),
        # # we'll always have at least two elements in a cube
        Column("El Cnt", type=int, getter=lambda col, row: len(row) - 9),
        ItemColumn("El 1", 8),
        ItemColumn("El 2", 9),
    ]

    def iterload(self):

        with self.source.open_text(encoding=self.options.encoding) as fp:

            # the log lines are comma delimited and double quoted
            rdr = csv.reader(remove_metadata_lines(fp))

            el_count = 2

            has_n = False
            has_s = False

            while True:
                try:

                    row = next(rdr)

                    cube = row[7]

                    # filter for specific cube if asked to
                    if self.tm1_cube and cube != self.tm1_cube:

                        continue

                    elif not self.tm1_ctrl and cube[0] == "}":

                        # only include control cubes if explicitly requested
                        # but if a control cube has be chosen as the filter cube
                        # implicitly they want it included

                        continue

                    # filter for specific user if asked to
                    user = row[3]

                    if self.tm1_user and user != self.tm1_user:

                        continue

                    # I think each log line has a trailing empty string for some reason
                    # row = row[:-1]

                    row_el_cols = len(row) - 9

                    while el_count < row_el_cols:

                        # we need to add all new columns

                        el_count = el_count + 1

                        col = ItemColumn(f"El {el_count}", el_count + 7)

                        self.addColumn(col)

                    # unhide value columns once type hit

                    if not has_n and row[4] == "N":
                        self.columns[4].width = 8
                        self.columns[5].width = 8

                    if not has_s and row[4] == "S":
                        self.columns[6].width = 8
                        self.columns[7].width = 8

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
