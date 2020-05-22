from datetime import datetime, timezone, timedelta
from eson.config import EsonExtension


class EsonDatetime(EsonExtension):
    def should_encode(self, value) -> bool:
        return isinstance(value, datetime)

    def encode(self, value):
        """Accepts a datetime object"""
        return {
            # Accurate to a micro second
            "timestamp": int(value.timestamp() * 1000000)
        }

    def decode(self, encoded_value):
        timestamp = encoded_value.get("timestamp")
        return datetime.fromtimestamp(timestamp / float(1000000))
