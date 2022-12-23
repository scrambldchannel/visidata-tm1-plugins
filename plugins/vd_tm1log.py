"""Allow VisiData to open TM1 transaction log files."""

__version__ = "0.1"

import csv

from visidata import vd, VisiData, SequenceSheet, options, stacktrace, Column, ColumnAttr
from visidata import TypedExceptionWrapper
import datetime
# vd.option('csv_lineterminator', '\r\n', 'lineterminator passed to csv.writer', replay=True)


@VisiData.api
def open_tm1log(vd, p):
    return TM1LogSheet(p.name, source=p)


class TM1LogSheet(SequenceSheet):

    _rowtype = "changes"  # rowdef: [str]

    # this isn't working
    columns = [
        # ColumnAttr('name'),  # foolib.Bar.name
        Column('Cube'),
    ]



    def iterload(self):

        with self.source.open_text(encoding=self.options.encoding) as fp:
            
            # skip first three lines
            fp.readline(3)  

        with self.source.open_text(encoding=self.options.encoding) as fp:

            # here we need to drop the first three lines

            # is this useful in any way?
            metadata = fp.readlines(3)

            # this is kinda useful, not sure how we can display it
            # This should be derived from the distinct values in the cube column anyway though
            # could maybe send a message somewhere in the ui though
            cubes_serialized = []

            while True:

                line = fp.readline()
                if line[0] == "#":
                    cubes_serialized.append(fp.readline())
                else:
                    break

            rdr = csv.reader(fp, **options.getall('csv_'))



            while True:
                try:

                    row = next(rdr)

                    # there's some sort of weird bug with the last line I think which gives 
                    # janky check to remove that weird trailing line
                    if len(row) < 8:
                        continue

                    # I think there's a start and an end but not sure if they ever change?
                    # I checked a couple of logs manually and didn't see a diff
                    
                    # naive parsing :shrug: - surely datetime supports this, will check
                    change_time = row[1]
                    change_time = datetime.datetime(year=int(change_time[:4]), month=int(change_time[4:6]), day=int(change_time[6:8]), hour=int(change_time[8:10]), minute=int(change_time[10:12]), second=int(change_time[12:14]))

                    user = row[3]
                    value_type = row[4]

                    # I'm in two minds about splitting string and numeric values into separate columns
                    # on one hand, it's a bit noisey, but on the other hand, it's nice to be able to treat numbers as numbers
                    # It might nice to be have an option to only include one or the other
                    n_value_before = None
                    n_value_after = None
                    s_value_before = None
                    s_value_after = None

                    if value_type == "N":
                        n_value_before = float(row[5])
                        n_value_after = float(row[6])
                    else:
                        s_value_before = row[5]
                        s_value_after = row[6]

                    cube = row[7]


                    # so the part I haven't quite worked out is how to split this variable length set of fields into columns
                    elements = row[8:]


                    yield [change_time, cube, user, value_type, n_value_before, n_value_after, s_value_before, s_value_after, elements]


                except csv.Error as e:
                    e.stacktrace=stacktrace()
                    yield [TypedExceptionWrapper(None, exception=e)]
                except StopIteration:
                    return  



vd.addGlobals({
    'TM1LogSheet': TM1LogSheet
})