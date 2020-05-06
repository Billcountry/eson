import json
import builtins


def encode(data, pretty=False):
    """Encode to an ESON string"""
    eson_data = __encode_types(data)
    if pretty:
        return json.dumps(eson_data, indent=4)
    return json.dumps(eson_data)


def __encode_types(data):
    _data = dict()
    if isinstance(data, dict):
        for key, value in data.items():
            encoded_key, encoded_value = __encode_type(key, value)
            if isinstance(encoded_value, (dict, list)):
                encoded_value = __encode_types(encoded_value)
            _data[encoded_key] = encoded_value

    if isinstance(data, list):
        _data['__eson-list__'] = __encode_types(dict(enumerate(data)))
    return _data


def __encode_type(key, value):
    config = getattr(builtins, "__eson_config__", dict())
    for name, extension in config.items():
        if extension.should_encode(value):
            encoded_key = '{name}~{key}'.format(name=name, key=key)
            encoded_value = extension.encode(value)
            return encoded_key, encoded_value
    return key, value

