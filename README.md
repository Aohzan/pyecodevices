# pyecodevices - Python GCE Eco-Devices

Get information from GCE Eco-Devices

## Parameters

- `host`: ip or hostname
- `port`: (default: 80)
- `username`: if authentication enabled on Eco-Devices
- `password`: if authentication enabled on Eco-Devices
- `request_timeout`: (default: 3)

## Properties

- `host`: return the host
- `firmware`: return the firmware version
- `mac_address`: return the mac address

## Methods

- `ping`: return true if the Eco-Devices answer
- `global_get`: return json from the API
- `get_t1`: return values of input T1
- `get_t2`: return values of input T2
- `get_c1`: return values of input C1
- `get_c2`: return values of input C2

## Example

```python
from pyecodevices import EcoDevices

import asyncio


async def main():
    async with EcoDevices('192.168.1.239', '80', "username", "password") as ecodevices:
        ping = await ecodevices.ping()
        print("ping:", ping)
        version = await ecodevices.firmware
        print("firmware version: ", version)
        data = await ecodevices.global_get()
        print("all values: ", data)
        data = await ecodevices.get_t1()
        print("teleinfo 1: ", data["current"])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```
