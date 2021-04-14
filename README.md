# pyecodevices - Python GCE Eco-Devices

Get information from GCE Eco-Devices

## Parameters

- `host`: ip or hostname
- `port`: (default: 80)
- `username`: if authentication enabled on Eco-Devices
- `password`: if authentication enabled on Eco-Devices
- `request_timeout`: (default: 10)

## Properties

- `host`: return the host
- `version`: return the firmware version
- `mac_address`: return the mac address

## Methods

- `get_info`: get properties from the API
- `global_get`: return all data from the API
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
        await ecodevices.get_info()
        print("firmware version:", ecodevices.version)
        data = await ecodevices.global_get()
        print("all values:", data)
        data = await ecodevices.get_t1()
        print("teleinfo 1:", data)
        print("current:", data["current"], "VA")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```
