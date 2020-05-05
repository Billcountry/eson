# ESON

This library allows you to implement extended JSON objects allowing you to 
share data between services, apps and languages as objects. The library comes with
built in extensions for date and datetime. You can write your own extensions to manage 
custom data.

This became a need for me when sharing data between two http services and being
forced to remember to do convert a timestamp back to datetime on each function handling
the data

## Getting Started

### Install
Run `pip install eson-py`

### Usage
Below is a summary of various operations using eson. 
[Click here](https://repl.it/@Billcountry/eson-python) to open a live test environment.

#### Encoding:
```python
from datetime import datetime, date
import eson

user = {
    "name": "Jane Doe",
    "date_of_birth": date.today(),
    "registered": datetime.now()
}

# Encoding the data
eson_data = eson.encode(user)

# Sample output
"""
{
    "name": "Jane Doe",
    "EsonDate~date_of_birth": {"year": 2020, "month": 04, "day": 10},
    "EsonDatetime~registered": {}
}
"""
```