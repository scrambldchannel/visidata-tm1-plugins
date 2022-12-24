# TM1 Transaction Log plugin for Visidata

Explore tm1 transaction logs with [Visidata](https://visidata.org).

## Install/Test

Copy `vd_tm1log.py` from the repo to 1 `/.visidata/plugins`

Add `import plugins.vd_tm1log` to `~/.visidatarc`

Generic instructions for installing plugins can be found [here](https://www.visidata.org/docs/plugins/).

Open a tm1 transaction log file with:

```sh
vd tm1s20200802093541.log -f tm1log
```
