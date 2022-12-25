# TM1 Transaction Log plugin for Visidata

Explore tm1 transaction logs with [Visidata](https://visidata.org).

## Installation

Copy `vd_tm1log.py` from the repo to 1 `~/.visidata/plugins`

Add `import plugins.vd_tm1log` to `~/.visidatarc`

Generic instructions for installing plugins can be found [here](https://www.visidata.org/docs/plugins/).

## Basic Usage

Open a tm1 transaction log file with:

```sh
vd tm1s20200802093541.log -f tm1log
```

Or open multiple logs at once:

```sh
vd tm1s20200802093541.log tm1s202009026084529.log -f tm1log
```

```sh
vd tm1s202012*.log -f tm1log
```


This will parse the log file(s) and show the cube changes in a custom Visidata sheet.


![ScreenShot](screenshot.png)

You then get all the power of Visidata at your fingertips.

E.g:

* Sort columns (Cubes, values, elements etc) with `[` and `]`
* Hide columns you're not interested in with `-`
* Select all rows matching where the value in the col matches the current selected cell with `,`
* Open all selected rows in a new sheet with `"` to help you zero in on a specific change

And much more, see the [Visidata cheat sheet](https://jsvine.github.io/visidata-cheat-sheet/en/).



## Options for Filtering

By default, control cubes are suppressed. You can include them with the `tm1-ctrl` option:

```sh
vd tm1s20200802093541.log -f tm1log --tm1-ctrl=true
```

You can also filter for a specific cube or user:

```sh
vd tm1s20200802093541.log -f tm1log --tm1-cube=sales
```

```sh
vd tm1s20200802093541.log -f tm1log --tm1-user=alexander.sutcliffe
```
**Note:** these filters are applied case _insensitively_ to mirror TM1's behaviour.

You can also choose to only include `N` or `S` values:

```sh
vd tm1s20200802093541.log -f tm1log --tm1-dt=n
```

You can also combine filters:

```sh
vd tm1s20200802093541.log -f tm1log --tm1-user=alexander.sutcliffe --tm1-cube=sales
```

Happy log hunting!
