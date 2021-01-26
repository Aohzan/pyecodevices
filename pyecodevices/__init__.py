"""Get information from GCE Eco-Devices."""
import requests
import xmltodict


class EcoDevices:
    """Class representing the Eco-Devices and its XML API."""

    def __init__(self, host, port=80, username=None, password=None, timeout=3):
        """Init a EcoDevice API."""
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._timeout = timeout
        self._api_url = f"http://{host}:{port}/status.xml"

    def _request(self):
        if self._username is not None and self._password is not None:
            r = requests.get(
                self._api_url,
                params={},
                auth=(self._username, self._password),
                timeout=self._timeout,
            )
        else:
            r = requests.get(self._api_url, params={}, timeout=self._timeout)
        r.raise_for_status()
        xml_content = xmltodict.parse(r.text)
        response = xml_content.get("response", None)
        if response:
            return response
        else:
            raise Exception(
                "Eco-Devices XML request error, url: %s`r%s",
                r.request.url,
                response,
            )

    @property
    def host(self):
        """Return the hostname."""
        return self._host

    @property
    def mac_address(self):
        """Return the mac address."""
        return self._request().get("config_mac")

    @property
    def firmware(self):
        """Return the firmware."""
        return self._request().get("version")

    def ping(self) -> bool:
        """Return true if Eco-Devices answer to API request."""
        try:
            self._request()
            return True
        except Exception:
            pass
        return False

    def global_get(self):
        """Return all values from API."""
        return self._request()

    def get_t1(self):
        """Get values from teleinformation 1 input."""
        data = self._request()
        return {
            "current": data.get("T1_PAPP"),
            "type_heures": data.get("T1_PTEC"),
            "souscription": data.get("T1_ISOUSC"),
            "intensite_max": data.get("T1_IMAX"),
        }

    def get_t2(self):
        """Get values from teleinformation 1 input."""
        data = self._request()
        return {
            "current": data.get("T2_PAPP"),
            "type_heures": data.get("T2_PTEC"),
            "souscription": data.get("T2_ISOUSC"),
            "intensite_max": data.get("T2_IMAX"),
        }

    def get_c1(self):
        """Get values from meter 1 input."""
        data = self._request()
        return {
            "daily": data.get("c0day"),
            "total": data.get("count0"),
            "fuel": data.get("c0_fuel"),
        }

    def get_c2(self):
        """Get values from meter 2 input."""
        data = self._request()
        return {
            "daily": data.get("c1day"),
            "total": data.get("count1"),
            "fuel": data.get("c1_fuel"),
        }
