# aircon-influx

A little application that queries echonetlite-compat air conditioners and sends the data to influxdb.

## Install

```bash
$ poetry install
```

or container:
```bash
$ podman build .
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

or with container:
```
$ cat <<EOF > .env
INFLUX_URL=http://influx_url.example.com:8086
INFLUX_BUCKET=bucket
INFLUX_TOKEN=secret
AIRCON_HOSTS=aircon1.local aircon2.local
EOF
$ podman run --rm -it --net=host --env-file .env ghcr.io/rene00/aircon-influx/aircon-influx:latest
Room temperature for host aircon1.local: 21
Room temperature for host aircon2.local: 20
```
