from visidata import AttrDict, vd


def load_vd_sheet(inpath, filetype=None):
    """Load a file and return the VisiData
    sheet object.
    """
    vd.loadConfigAndPlugins(AttrDict({}))
    sheet = vd.openSource(inpath, filetype=filetype)
    sheet.reload()
    vd.sync()
    return sheet
