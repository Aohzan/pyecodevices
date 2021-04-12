"""Get information from GCE Eco-Devices."""
import asyncio
import socket

import aiohttp
import async_timeout
import xmltodict


class EcoDevices:
    """Class representing the Eco-Devices and its XML API."""

    def __init__(
        self,
        host: str,
        port: int = 80,
        username: str = None,
        password: str = None,
        request_timeout: int = 10,
        session: aiohttp.client.ClientSession = None,
    ) -> None:
        """Init a EcoDevice API."""
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._request_timeout = request_timeout
        self._api_url = f"http://{host}:{port}/status.xml"
        self._version = None
        self._mac_address = None

        self._session = session
        self._close_session = False

    async def get_info(self):
        """Get properties from API."""
        init_data = await self._request()
        self._version = init_data["version"]
        self._mac_address = init_data["config_mac"]

    async def _request(self) -> dict:
        """Make a request to get Eco-Devices data."""
        auth = None
        if self._username and self._password:
            auth = aiohttp.BasicAuth(self._username, self._password)

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        try:
            with async_timeout.timeout(self._request_timeout):
                response = await self._session.request(
                    "GET",
                    self._api_url,
                    auth=auth,
                    data=None,
                    json=None,
                    params=None,
                    headers={},
                    ssl=False,
                )
        except asyncio.TimeoutError as exception:
            raise EcoDevicesCannotConnectError(
                "Timeout occurred while connecting to Eco-Devices."
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise EcoDevicesCannotConnectError(
                "Error occurred while communicating with Eco-Devices."
            ) from exception
        if response.status == 401:
            raise EcoDevicesInvalidAuthError("Authentication failed with Eco-Devices.")

        if response.status:
            contents = await response.text()
            response.close()
            xml_content = xmltodict.parse(contents)
            data = xml_content.get("response", None)
            if data:
                return data
            raise EcoDevicesCannotConnectError("Eco-Devices XML request error:", data)

    @property
    def host(self) -> str:
        """Return the hostname."""
        return self._host

    @property
    def mac_address(self) -> str:
        """Return the mac address."""
        return self._mac_address

    @property
    def version(self) -> str:
        """Return the firmware version."""
        return self._version

    async def global_get(self) -> dict:
        """Return all values from API."""
        return await self._request()

    async def get_t1(self) -> dict:
        """Get values from teleinformation 1 input."""
        data = await self._request()
        return {
            "current": data.get("T1_PAPP"),
            "type_heures": data.get("T1_PTEC"),
            "souscription": data.get("T1_ISOUSC"),
            "intensite_max": data.get("T1_IMAX"),
        }

    async def get_t2(self) -> dict:
        """Get values from teleinformation 1 input."""
        data = await self._request()
        return {
            "current": data.get("T2_PAPP"),
            "type_heures": data.get("T2_PTEC"),
            "souscription": data.get("T2_ISOUSC"),
            "intensite_max": data.get("T2_IMAX"),
        }

    async def get_c1(self) -> dict:
        """Get values from meter 1 input."""
        data = await self._request()
        return {
            "daily": data.get("c0day"),
            "total": data.get("count0"),
            "fuel": data.get("c0_fuel"),
        }

    async def get_c2(self) -> dict:
        """Get values from meter 2 input."""
        data = await self._request()
        return {
            "daily": data.get("c1day"),
            "total": data.get("count1"),
            "fuel": data.get("c1_fuel"),
        }

    async def close(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self):
        """Async enter."""
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit."""
        await self.close()


class EcoDevicesCannotConnectError(Exception):
    """Exception to indicate an error in connection."""


class EcoDevicesInvalidAuthError(Exception):
    """Exception to indicate an error in authentication."""
