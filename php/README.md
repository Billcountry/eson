# Extended JSON(ESON)

![PHP Tests](https://github.com/Billcountry/eson/workflows/PHP%20Tests/badge.svg?branch=master)

JSON is great for sharing data in a human readable format but sometimes it lacks in object types support.
ESON does not re-invent the wheel, it just provides a base for you to implement extended JSON objects allowing you to
share data between services, apps and languages as objects.

ESON comes with built in extensions for date and datetime. You can write your own extensions to manage
custom data.

This is the PHP version of ESON. See other languages [here](https://github.com/Billcountry/eson#languages).

## Getting Started
**Note**: PHP doesn't support date and datetime as separate entities. It can **decode date and datetime** objects but it **encodes datetime** even for what was originally an ESON date object.

ESON is safe to use in a browser, web workers and in node-js.

### Install
Run `composer install eson`

### Usage
Below is a summary of various operations using eson. 
<a href="https://repl.it/@Billcountry/eson-php" target="_blank">Click here for a live IDE.</a>

#### Encoding:
```php
use ESON;

$user = array(
    "name" => "Jane Doe",
    "date_of_birth" => new DateTime("20-04-2020"),
    "registered" => new DateTime()
);

// Encoding the data (True argument to make it pretty. Not required)
$eson_data = ESON::encode($user, true);
echo $eson_data;

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
```php
use ESON;

$eson_data = '{"EsonDatetime~datetime": {"timestamp": 1588822240000400}, "array": ["Some string",0,{"EsonDatetime~":{"timestamp":1588822240400000}},false,null]}';
$data = ESON::decode($eson_data);

var_dump($data);
```

#### Extending ESON
You can extend ESON to achieve various purposes, e.g loading a database entity when you recieve it's ID

An extension should have the keys `should_encode`, `encode`, `decode` and `name`. Below is the sample code used to extend Datetime objects in ESON
```php
use ESON;

// Define the extension
$EsonDatetime = array(
    "name" => "EsonDatetime",
    "should_encode" => function ($value) {
        return $value instanceof DateTime;
    },
    "encode" => function ($value) {
        return array("timestamp" => $value->getTimestamp() * 1000000);
    },
    "decode" => function ($value) {
        $ts = $value["timestamp"];
        $dt = new DateTime();
        $dt->setTimestamp(intval($ts / 1000000));
        return $dt;
    }
);
```

Once an extension is created, at the entry of your application add the extension to ESON
```php
use ESON;

ESON::add_extension($EsonDatetime);
```

That's it, your extension is ready to encode objects.
