# aircon-influx

A little application that queries echonetlite-compat air conditioners and sends the data to influxdb.

## Install

```bash
$ poetry install
```

## Usage

```bash
$ INFLUX_URL=http://influx_url.example.com:8086 \
    INFLUX_BUCKET=bucket \
    INFLUX_TOKEN=secret \
    AIRCON_HOSTS="aircon1.local aircon2.local" \
    poetry run python ./app.py
Room temperature for host aircon1.local: 21
Room temperature for host aircon2.local: 20
```
