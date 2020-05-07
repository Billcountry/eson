import logging
import builtins
import json


def decode(encoded_data):
    """Decode an ESON string to the original object"""
    data = json.loads(encoded_data)
    return __decode_types(data)


def __decode_types(data):
    if isinstance(data, dict):
        _data = dict()
        for encoded_key, encoded_value in data.items():
            key, value = __decode_type(encoded_key, encoded_value)
            if isinstance(value, (dict, list)):
                value = __decode_types(value)
            if not key:
                return value
            _data[key] = value
        return _data            

    if isinstance(data, list):
        _data = list()
        for value in data:
            if isinstance(value, (dict, list)):
                value = __decode_types(value)
            _data.append(value)
        return _data
    
    return data


def __decode_type(encoded_key, encoded_value):
    key_parts = encoded_key.split("~")
    if len(key_parts) != 2:
        return encoded_key, encoded_value
    config = getattr(builtins, "__eson_config__", dict())
    extension_name, key = key_parts
    extension = config.get(extension_name)
    if extension:
        return key, extension.decode(encoded_value)
    logging.warning("Missing ESON configuration for %s", extension_name)
    return encoded_key, encoded_value
