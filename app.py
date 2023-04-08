import asyncio
import socket
import os
from datetime import datetime
from typing import List, Union, Dict
from influxdb_client.client.write_api import SYNCHRONOUS, WriteApi
from pychonet.lib.udpserver import UDPServer
from pychonet import ECHONETAPIClient, HomeAirConditioner
from pychonet import ECHONETAPIClient as api
from influxdb_client import InfluxDBClient, Point


async def main(hosts: List[str], **kwargs) -> None: 

    influx_client: Union[InfluxDBClient, None] = None
    write_api: Union[WriteApi, None] = None
    influx_token: Union[str, None] = kwargs.get("influx_token", None)
    influx_bucket: Union[str, None] = kwargs.get("influx_bucket", None)
    influx_url: Union[str, None] = kwargs.get("influx_url", None)
    influx_org: Union[str, None] = kwargs.get("influx_org", None)

    udp: UDPServer = UDPServer()
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    udp.run("0.0.0.0", 3610, loop=loop)
    server: ECHONETAPIClient = api(server=udp)

    if all(v is not None for v in (influx_token, influx_bucket, influx_url, influx_org)):
        influx_client = InfluxDBClient(url=str(influx_url), token=str(influx_token))
        write_api = influx_client.write_api(write_options=SYNCHRONOUS)

    for host in hosts:
        try:
            ip_address: str = socket.gethostbyname(host)
        except socket.gaierror as e:
            print(f"Failed to resolve hostname {host}: {e}")
            continue

        # Discover ECHONETLite instances
        await server.discover(ip_address)

        # Populate the property map for the ECHONETLite instance
        await server.getAllPropertyMaps(ip_address, 1, 48, 1)

        # Create a HomeAirConditioner instance using the Factory
        aircon: HomeAirConditioner = HomeAirConditioner(ip_address, server)

        # Get the room temperature
        room_temperature_bytes: Union[bytes, bool] = await aircon.getRoomTemperature()
        if not room_temperature_bytes:
            print(f"Failed to retrieve room temperature for host {host}")
            continue

        room_temperature_bytes = bytes(room_temperature_bytes)
        room_temperature: int = int.from_bytes(bytes(room_temperature_bytes), byteorder='big')
        print(f"Room temperature for host {host}: {room_temperature}")

        if write_api:
            point: Point = Point("room_temperature").tag("host", host).field("temperature", room_temperature).time(datetime.utcnow())
            write_api.write(str(influx_bucket), influx_org, point)


if __name__ == '__main__':
    hosts: List[str] = os.environ.get("AIRCON_HOSTS", "").split()
    influx_url: str = os.environ.get("INFLUX_URL", "")
    influx_token: str = os.environ.get("INFLUX_TOKEN", "")
    influx_bucket: str = os.environ.get("INFLUX_BUCKET", "")
    influx_org: str = os.environ.get("INFLUX_ORG", "")
    kwargs: Dict[str, str] = {
        "influx_url": influx_url,
        "influx_token": influx_token,
        "influx_bucket": influx_bucket,
        "influx_org": influx_org,
    }

    asyncio.run(main(hosts, kwargs=kwargs))
