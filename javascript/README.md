# Extended JSON(ESON)

![Javascript Tests](https://github.com/Billcountry/eson/workflows/Javascript%20Tests/badge.svg?branch=master)

JSON is great for sharing data in a human readable format but sometimes it lacks in object types support.
ESON does not re-invent the wheel, it just provides a base for you to implement extended JSON objects allowing you to
share data between services, apps and languages as objects.

ESON comes with built in extensions for date and datetime. You can write your own extensions to manage
custom data.

This is the javascript version of ESON. See other languages [here](https://github.com/Billcountry/eson#languages)

## Getting Started
**Note**: Javascript doesn't support date and datetime as separate entities. It can **decode date and datetime** objects but it **encodes datetime** even for what was originally an ESON date object.

ESON is safe to use in browser, webworkers and in node-js.

### Install
Run `npm install eson-js`
Yarners `yarn add eson-js`

### Usage
Below is a summary of various operations using eson. 
<a href="https://repl.it/@Billcountry/eson-javascript" target="_blank">Click here for a live IDE.</a>

#### Encoding:
```js
const eson = require("eson-js")

const user = {
    name: "Jane Doe",
    date_of_birth: new Date(2020, 3, 20),
    registered: new Date()
}

// Encoding the data (True argument to make it pretty. Not required)
const eson_data = eson.encode(user, true)
console.log(eson_data)

// Sample output
/*
{
    "name": "Jane Doe",
    "EsonDate~date_of_birth": {"year": 2020, "month": 04, "day": 10},
    "EsonDatetime~registered": {...}
}
*/
```

#### Decoding
```js
const eson = require("eson-js")

const eson_data = '{"EsonDatetime~datetime": {"timestamp": 1588822240000400}, "array": ["Some string",0,{"EsonDatetime~":{"timestamp":1588822240400000}},false,null]}'
const data = eson.decode(eson_data)

console.log(data)
```

#### Extending ESON
You can extend ESON to achieve various purposes, e.g loading a database entity when you recieve it's ID

An extension should have the keys `should_encode`, `encode`, `decode` and `name`. Below is the sample code used to extend Datetime objects in ESON
```js
const eson = require("eson-js")

exports.EsonDatetime = {
    name: "EsonDatetime",
    should_encode: value => value instanceof Date,
    encode: value => {
        // ESON processes datetime in micro-seconds
        return {
            timestamp: value.getTime() * 1000,
        }
    },
    decode: value => new Date(value.timestamp / 1000),
}
```

Once an extension is created, at the entry of your application add the extension to ESON
```js
const eson = require("eson-js")

eson.add_extension(EsonDatetime)
```

That's it, your extension is ready to encode objects.
