# pyecodevices - Python GCE Eco-Devices

Get information from GCE Eco-Devices

## Parameters

- `host`: ip or hostname
- `port`: (default: 80)
- `username`: if authentication enabled on Eco-Devices
- `password`: if authentication enabled on Eco-Devices
- `timeout`: (default: 3)

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

ecodevices = EcoDevices('192.168.1.239','80',"username","password")

print("# ping")
print(ecodevices.ping())
print("# firmware version")
print(ecodevices.firmware)
print("# all values")
print(ecodevices.global_get())
print("# inputs values")
print(ecodevices.get_t1())
print(ecodevices.get_t2())
print(ecodevices.get_c1())
print(ecodevices.get_c2())
```
