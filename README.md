# pyecodevices - Python GCE Eco-Devices

Get information from GCE Eco-Devices

## Parameters

- `host`: ip or hostname
- `port`: (default: 80)
- `username`: if authentication enabled
- `password`: if authentication enabled
- `timeout`: (default: 3)

## Methods

- `ping`: return true if the Eco-Devices answer
- `global_get`: return json from the API
- `get`: return value of key parameter in: `current_t1`, `current_t2`, `daily_c1`, `daily_c2`, `total_c1`, `total_c2`

## Example

```python
from pyecodevices import EcoDevices

ecodevices = EcoDevices('192.168.1.239','80',"username","password")
print (ecodevices.ping())
print (ecodevices.global_get())
print (ecodevices.get("current_t1"))
```
