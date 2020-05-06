from datetime import datetime, timezone, timedelta
from eson.config import EsonExtension


class EsonDatetime(EsonExtension):
    def should_encode(self, value) -> bool:
        return isinstance(value, datetime)

    def encode(self, value):
        """Accepts a datetime object"""
        encoded_object = {
            # Accurate to a micro second
            "timestamp": int(value.timestamp() * 1000000)
        }
        if value.tzinfo:
            encoded_object["timezone"] = {
                "offset": int(value.tzinfo.utcoffset(value).total_seconds()),
                "name": value.tzinfo.tzname(value)
            }
        return encoded_object

    def decode(self, encoded_value):
        timestamp = encoded_value.get("timestamp")
        tz = encoded_value.get("timezone")
        dt = datetime.fromtimestamp(timestamp / float(1000000))
        if tz:
            offset = tz.get("offset")
            name = tz.get("name")
            tzinfo = timezone(timedelta(seconds=offset), name)
            dt = dt.replace(tzinfo=tzinfo)
        return dt
