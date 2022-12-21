"""Allow VisiData to open TM1 transaction log files."""

__version__ = "0.1"

from visidata import (
    asyncthread,
#     vd,
#     ColumnItem,
#     deduceType,
    VisiData,
    PythonSheet,
)

@VisiData.api
def open_toml(vd, p):
    return TomlSheet(p.name, source=p)


class TomlSheet(PythonSheet):
    """A Sheet representing the entries in a TM1 transaction log file.

    """

    rowtype = "values"  # rowdef: dict values, possibly nested

    @asyncthread
    def reload(self):
        """Loading a TOML file produces a single dict. Use
        its keys as column headings, and populate a single
        row.
        """
        self.columns = []
        self.rows = []

        data = tomllib.load(self.source.open_bytes())
        for k, v in data.items():
            self.addColumn(ColumnItem(k, type=deduceType(v)))
        self.addRow(data)


vd.addGlobals(vd.getGlobals())
