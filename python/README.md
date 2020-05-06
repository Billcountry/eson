# Extended JSON(ESON)
JSON is great for sharing data in a human readable format but sometimes it lacks in object types support.
ESON does not re-invent the wheel, it just provides a base for you to implement extended JSON objects allowing you to
share data between services, apps and languages as objects.

ESON comes with built in extensions for date and datetime. You can write your own extensions to manage
custom data.

This is the python version of ESON. See other languages [here](https://github.com/Billcountry/eson#languages)

## Getting Started

### Install
Run `pip install eson`

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
eson_data = eson.encode(user, pretty=True)

# Sample output
"""
{
    "name": "Jane Doe",
    "EsonDate~date_of_birth": {"year": 2020, "month": 04, "day": 10},
    "EsonDatetime~registered": {...}
}
"""
```

#### Decoding
```python
import eson

# A timezone aware date object
eson_data = '{"EsonDatetime~eatime": {"timestamp": 1588822240000400, "timezone": {"offset": 10800, "name": "EAT"}}}'
data = eson.decode(eson_data)

print(data.get("eatime"))
# Expected output '2020-05-07 06:30:40.000400+03:00'
```

#### Extending ESON
You can extend ESON to achieve various purposes, e.g loading a database entity when you recieve it's ID

Below is the sample code used to extend Date objects in ESON
```python
from datetime import date
from eson import EsonExtension

class EsonDate(EsonExtension):
    # Extend this method, use it to check whether you should encode this value
    def should_encode(self, value) -> bool:
        return type(value) == date

    def encode(self, value):
        # Encode your value to valid JSON object
        return dict(year=value.year, month=value.month, day=value.day)

    def decode(self, encoded_value):
        # Decode your object to an object relevant to your application
        return date(**encoded_value)
```

Once an extension is created, at the entry of your application add the extension to ESON
```python
import eson

eson.add_extension(EsonDate)
```

That's it, your extension is ready to encode objects.
