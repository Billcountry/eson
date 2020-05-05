"""Extended JSON

This package is meant to provide a more flexible version of JSON supporting more data types
By default it comes with built-in support for date and time objects

It can be easily configured to support other objects
"""
from eson.encoder import encode
from eson.decoder import decode
from eson.config import EsonExtension, add_extension
from eson.extensions.date import EsonDate
from eson.extensions.datetime import EsonDatetime


# Configure builtin extensions
add_extension(EsonDate())
add_extension(EsonDatetime())
