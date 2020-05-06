import logging
import builtins
import json


def decode(encoded_data):
    """Decode an ESON string to the original object"""
    data = json.loads(encoded_data)
    return __decode_types(data)


def __decode_types(data):
    if not isinstance(data, dict):
        return data
    # Decode a list correctly back to a list
    is_list = '__eson-list__' in data
    _data = dict()
    if is_list:
        _data = list()
        data = data['__eson-list__']
    for encoded_key, encoded_value in data.items():
        key, value = __decode_type(encoded_key, encoded_value)
        if isinstance(value, dict):
            value = __decode_types(value)
        if is_list:
            _data.append(value)
        else:
            _data[key] = value
    return _data


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
