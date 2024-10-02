"""Basic testing file."""

import asyncio
import os

from pyecodevices import EcoDevices

ED_HOST = os.environ["ED_HOST"]
ED_PASSWORD = os.environ["ED_PASSWORD"]


async def main():
    """Test the EcoDevices."""
    async with EcoDevices(ED_HOST, "80", "admin", ED_PASSWORD) as ecodevices:
        await ecodevices.get_info()
        print("firmware version:", ecodevices.version)
        data = await ecodevices.global_get()
        print("all values:", data)
        data = await ecodevices.get_t1()
        print("teleinfo 1:", data)
        print("current:", data["current"], "VA")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
