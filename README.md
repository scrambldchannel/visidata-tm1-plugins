# TM1 Transaction Log plugin for Visidata

Explore tm1 transaction logs with [Visidata](https://visidata.org).

## Installation

Copy `vd_tm1log.py` from the repo to 1 `/.visidata/plugins`

Add `import plugins.vd_tm1log` to `~/.visidatarc`

Generic instructions for installing plugins can be found [here](https://www.visidata.org/docs/plugins/).

## Basic Usage

Open a tm1 transaction log file with:

```sh
vd tm1s20200802093541.log -f tm1log
```

## Options for Filtering

By default, control cubes are suppressed. You can include them with the `tm1-ctrl` option:

```sh
vd tm1s20200802093541.log -f tm1log --tm1-ctrl=true
```

You can also filter for a specific cube or user:

```sh
vd tm1s20200802093541.log -f tm1log --tm1-cube=Sales
```

```sh
vd tm1s20200802093541.log -f tm1log --tm1-user=alexander.sutcliffe
```

You can also filter by both:

```sh
vd tm1s20200802093541.log -f tm1log --tm1-user=alexander.sutcliffe --tm1-cube=Sales
```

Happy log hunting!
