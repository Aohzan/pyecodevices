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
        self._api_teleinfo_1_url = (
            f"http://{host}:{port}/protect/settings/teleinfo1.xml"
        )
        self._api_teleinfo_2_url = (
            f"http://{host}:{port}/protect/settings/teleinfo2.xml"
        )
        self._version = None
        self._mac_address = None

        self._session = session
        self._close_session = False

    async def get_info(self):
        """Get properties from API."""
        init_data = await self._request(self._api_url)
        self._version = init_data["version"]
        self._mac_address = init_data["config_mac"]

    async def _request(self, url: str) -> dict:
        """Make a request to get Eco-Devices data."""
        auth = None
        if self._username and self._password:
            auth = aiohttp.BasicAuth(self._username, self._password)

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        try:
            with async_timeout.timeout(self._request_timeout):
                response = await self._session.get(url, auth=auth)
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
    def port(self) -> int:
        """Return the port."""
        return self._port

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
        result = await self._request(self._api_url)
        result.update(await self._request(self._api_teleinfo_1_url))
        result.update(await self._request(self._api_teleinfo_2_url))
        return result

    async def get_t1(self) -> dict:
        """Get values from teleinformation 1 input."""
        data = await self._request(self._api_teleinfo_1_url)
        return {
            "current": data.get("T1_PAPP"),
            "type_heures": data.get("T1_PTEC"),
            "souscription": data.get("T1_ISOUSC"),
            "intensite_max": data.get("T1_IMAX"),
            "intensite_max_ph1": data.get("T1_IMAX1"),
            "intensite_max_ph2": data.get("T1_IMAX2"),
            "intensite_max_ph3": data.get("T1_IMAX3"),
            "intensite_now": data.get("T1_IINST"),
            "intensite_now_ph1": data.get("T1_IINST1"),
            "intensite_now_ph2": data.get("T1_IINST2"),
            "intensite_now_ph3": data.get("T1_IINST3"),
            "numero_compteur": data.get("T1_ADCO"),
            "option_tarifaire": data.get("T1_OPTARIF"),
            "index_base": data.get("T1_BASE"),
            "index_heures_creuses": data.get("T1_HCHC"),
            "index_heures_pleines": data.get("T1_HCHP"),
            "index_heures_normales": data.get("T1_EJPHN"),
            "index_heures_pointes": data.get("T1_EJPHPM"),
            "preavis_heures_pointes": data.get("T1_PEJP"),
            "groupe_horaire": data.get("T1_HHPHC"),
            "index_heures_creuses_jour_bleu": data.get("T1_BBRHCJB"),
            "index_heures_pleines_jour_bleu": data.get("T1_BBRHPJB"),
            "index_heures_creuses_jour_blanc": data.get("T1_BBRHCJW"),
            "index_heures_pleines_jour_blanc": data.get("T1_BBRHPJW"),
            "index_heures_creuses_jour_rouge": data.get("T1_BBRHCJR"),
            "index_heures_pleines_jour_rouge": data.get("T1_BBRHPJR"),
            "etat": data.get("T1_MOTDETAT"),
        }

    async def get_t2(self) -> dict:
        """Get values from teleinformation 2 input."""
        data = await self._request(self._api_teleinfo_2_url)
        return {
            "current": data.get("T2_PAPP"),
            "type_heures": data.get("T2_PTEC"),
            "souscription": data.get("T2_ISOUSC"),
            "intensite_max": data.get("T2_IMAX"),
            "intensite_max_ph1": data.get("T2_IMAX1"),
            "intensite_max_ph2": data.get("T2_IMAX2"),
            "intensite_max_ph3": data.get("T2_IMAX3"),
            "intensite_now": data.get("T2_IINST"),
            "intensite_now_ph1": data.get("T2_IINST1"),
            "intensite_now_ph2": data.get("T2_IINST2"),
            "intensite_now_ph3": data.get("T2_IINST3"),
            "numero_compteur": data.get("T2_ADCO"),
            "option_tarifaire": data.get("T2_OPTARIF"),
            "index_base": data.get("T2_BASE"),
            "index_heures_creuses": data.get("T2_HCHC"),
            "index_heures_pleines": data.get("T2_HCHP"),
            "index_heures_normales": data.get("T2_EJPHN"),
            "index_heures_pointes": data.get("T2_EJPHPM"),
            "preavis_heures_pointes": data.get("T2_PEJP"),
            "groupe_horaire": data.get("T2_HHPHC"),
            "index_heures_creuses_jour_bleu": data.get("T2_BBRHCJB"),
            "index_heures_pleines_jour_bleu": data.get("T2_BBRHPJB"),
            "index_heures_creuses_jour_blanc": data.get("T2_BBRHCJW"),
            "index_heures_pleines_jour_blanc": data.get("T2_BBRHPJW"),
            "index_heures_creuses_jour_rouge": data.get("T2_BBRHCJR"),
            "index_heures_pleines_jour_rouge": data.get("T2_BBRHPJR"),
            "etat": data.get("T2_MOTDETAT"),
        }

    async def get_c1(self) -> dict:
        """Get values from meter 1 input."""
        data = await self._request(self._api_url)
        return {
            "daily": data.get("c0day"),
            "total": data.get("count0"),
            "fuel": data.get("c0_fuel"),
        }

    async def get_c2(self) -> dict:
        """Get values from meter 2 input."""
        data = await self._request(self._api_url)
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
