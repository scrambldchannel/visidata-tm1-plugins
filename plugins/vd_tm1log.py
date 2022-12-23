mport csv

from visidata import vd, VisiData, TableSheet, options, stacktrace, Column, ColumnAttr
from visidata import TypedExceptionWrapper
import datetime

# vd.option('csv_lineterminator', '\r\n', 'lineterminator passed to csv.writer', replay=True)


@VisiData.api
def open_tm1log(vd, p):
    return TM1LogSheet(p.name, source=p)

def remove_metadata_lines(fp):
    
    # there are metadata lines in the file that we want to skip
    # all such lines start with a #, sometimes with a leading space
    # there's a trailing with a single weird char (this can be handled more elegantly surely)
    for line in fp:

        if line[0] ==  "#" or len(line) == 1 or line[1] == "#":
            continue
        else:
            yield line


class TM1LogRow(TableSheet):

    def __init__(self, row):

        # must be a better way... 
        self.time = datetime.datetime(year=int(row[2][:4]), month=int(row[2][4:6]), day=int(row[2][6:8]), hour=int(row[2][8:10]), minute=int(row[2][10:12]), second=int(row[2][12:14]))

        self.cube = row[7]
        self.user = row[3]
        self.type = row[4]

        # I'm in two minds about splitting string and numeric values into separate columns
        # on one hand, it's a bit noisey, but on the other hand, it's nice to be able to treat numbers as numbers
        # It might nice to be have an option to only include one or the other
        self.old_n = None
        self.old_s = None
        self.new_n = None
        self.new_s = None

        # it would be nice to be able to suppress completely null columns
        if self.type == "N":
            self.old_n = float(row[5])
            self.new_n = float(row[6])
        else:
            self.old_s = row[5]
            self.new_s = row[6]

        self.el_1 = row[8]
        self.el_2 = row[9]



class TM1LogSheet(TableSheet):

    rowtype = "changes"  # rowdef: list



    # create

    columns = [
            Column('Time', type=str, width=21, getter=lambda col,row: row.time), # how to date format this? 
            Column('Cube', type=str, width=30, getter=lambda col,row: row.cube),
            Column('User', type=str, width=20, getter=lambda col,row: row.user),
            Column('T', type=str, width=3, getter=lambda col,row: row.type),
            Column('Old Val N', width=14, type=float, getter=lambda col,row: row.old_n),
            Column('New Val N', width=14, type=float, getter=lambda col,row: row.new_n),
            Column('Old Val S', width=14, type=str, getter=lambda col,row: row.old_s),
            Column('New Val S', width=14, type=str, getter=lambda col,row: row.new_s),
            # we'll always have at least two elements in a cube
            Column('El 1', width=14, type=str, getter=lambda col,row: row.el_1),
            Column('El 2', width=14, type=str, getter=lambda col,row: row.el_2),
            # need to add the further columns

        ]

    
    def iterload(self):



        with self.source.open_text(encoding=self.options.encoding) as fp:

            # the log lines are comma delimited and double quoted
            rdr = csv.reader(remove_metadata_lines(fp))


            # we always have at least 2 elements in any cube
            # increment this as we find more
            el_start = 8
            el_cols = 2

            while True:
                try:

                    row = next(rdr)

                    # set max el count
                    el_cols_row = len(row[el_start:]) + 1

                    el_cols = max(el_cols, el_cols_row)

                    yield TM1LogRow(row)

                except csv.Error as e:
                    e.stacktrace=stacktrace()
                    yield [TypedExceptionWrapper(None, exception=e)]
                except StopIteration:
                    return  

# not sure where this should be done / or whether there's a better way to achieve this
TM1LogSheet.class_options.header = 0

vd.addGlobals({
    'TM1LogSheet': TM1LogSheet
})