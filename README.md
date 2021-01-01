# File Based Local Storage (CRD Support)

## Pre-requisite

- Python3

## Supported OS

- Supported in all OS systems

## How to import & use

```python3
from LocalStorage import LocalStorage

# Initialization
localstorage = Localstorage()
# or
localstorage = Localstorage("/Users/admin") # Custom path to store the file, MUST BE ONLY DIRECTORY & NOT FILENAME

# Create a Key Value
localstorage.create("Keyname", {"value": "Should be json type"})

# Get a Value from Key, Returns the value
localstorage.get("Keyname")

# Delete the Key
localstorage.delete("Keyname")
```
