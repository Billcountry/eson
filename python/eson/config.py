import builtins
from abc import ABC, abstractmethod


def add_extension(extension):
    if not isinstance(extension, EsonExtension):
        raise Exception("Extension must be an instance of an EsonExtension ancestor")

    config = getattr(builtins, "__eson_config__", dict())
    config[extension.__class__.__name__] = extension
    setattr(builtins, "__eson_config__", config)


class EsonExtension(ABC):
    @abstractmethod
    def should_encode(self, value) -> bool:
        """Returns bool if the value should be encoded by this extension"""
        pass

    @abstractmethod
    def encode(self, value):
        """Logic used to encode the object to a valid JSON object"""
        pass

    @abstractmethod
    def decode(self, encoded_value):
        """Logic used to decode the object from a json object to a valid python object"""
        pass
