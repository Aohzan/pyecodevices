# pyecodevices - Python GCE Eco-Devices

Get information from GCE Eco-Devices

## Parameters

- host: ip or hostname
- port: (default: 80)
- username: if authentication enabled
- password: if authentication enabled
- timeout: (default: 3)

## Example

```python
from pyecodevices import EcoDevices

ecodevices = EcoDevices('192.168.1.239','80',"username","password")
print (ecodevices.ping())
print (ecodevices.global_get())
print (ecodevices.get("current_t1"))
```
