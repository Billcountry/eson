import unittest
import eson
import json
from datetime import datetime, date, timezone, timedelta


class TestCase(unittest.TestCase):
    def test_simple_encode(self):
        normal_dict = dict(name="Jane Doe", sibling="Jane Doe")
        self.assertEqual(json.dumps(normal_dict), eson.encode(normal_dict))

    def test_simple_decode(self):
        json_data = '{"name": "Jane Doe"}'
        self.assertEqual(eson.decode(json_data), dict(name="Jane Doe"))

    def test_list_backward_compatibility(self):
        some_json_list = "[1, 2, 3]"
        self.assertEqual(eson.decode(some_json_list), [1, 2, 3])

    def test_list_encode(self):
        a_list = [1, 2, 3]
        expected_eson = '{"__eson-list__": {"0": 1, "1": 2, "2": 3}}'
        self.assertEqual(eson.encode(a_list), expected_eson)

    def test_list_decode(self):
        eson_data = '{"__eson-list__": {"0": 1, "1": 2, "2": 3, "3": "Some String"}}'
        expected_list = [1, 2, 3, "Some String"]
        self.assertEqual(eson.decode(eson_data), expected_list)

    def test_date_encode(self):
        data = dict(dob=date(year=2020, month=4, day=20), name="Corona")
        expected_eson = '{"EsonDate~dob": {"year": 2020, "month": 4, "day": 20}, "name": "Corona"}'
        self.assertEqual(eson.encode(data), expected_eson)

    def test_date_decode(self):
        eson_data = '{"EsonDate~dob": {"year": 1969, "month": 4, "day": 20}, "height": 30}'
        expected_data = dict(dob=date(year=1969, month=4, day=20), height=30)
        self.assertEqual(eson.decode(eson_data), expected_data)

    def test_datetime_encode(self):
        dt = datetime(year=2020, month=5, day=7, hour=6, minute=30, second=40, microsecond=400)
        data = dict(registered=dt, username="bear")
        expected_eson = '{"EsonDatetime~registered": {"timestamp": 1588822240000400}, "username": "bear"}'
        self.assertEqual(eson.encode(data), expected_eson)
        # Timezone aware datetime objects
        tz = timezone(timedelta(hours=3), "EAT")
        dtz = datetime(year=2020, month=5, day=7, hour=6, minute=30, second=40, microsecond=400, tzinfo=tz)
        expected_eson = '{"EsonDatetime~eatime": ' \
                        '{"timestamp": 1588822240000400, "timezone": {"offset": 10800, "name": "EAT"}}, ' \
                        '"username": "bear"}'
        data = dict(eatime=dtz, username="bear")
        self.assertEqual(eson.encode(data), expected_eson)

    def test_datetime_decode(self):
        dt = datetime(year=2020, month=5, day=7, hour=6, minute=30, second=40, microsecond=400)
        eson_data = '{"EsonDatetime~date_of_birth": {"timestamp": 1588822240000400}, "horoscope": "taurus"}'
        self.assertEqual(dict(date_of_birth=dt, horoscope="taurus"), eson.decode(eson_data))
        # Decode a timezone aware date
        eson_data = '{"EsonDatetime~eatime": {"timestamp": 1588822240000400, "timezone": {"offset": 10800, "name": "Africa/Nairobi"}}}'
        tz = timezone(timedelta(hours=3), "Africa/Nairobi")
        dtz = datetime(year=2020, month=5, day=7, hour=6, minute=30, second=40, microsecond=400, tzinfo=tz)
        data = eson.decode(eson_data)
        self.assertEqual(dtz, data.get("eatime"))
    
    def test_combined_list_data_encode(self):
        d = date(year=2020, month=4, day=20)
        dt = datetime(year=2020, month=5, day=7, hour=6, minute=30, second=40, microsecond=400)
        data = dict(name="Jane Doe", log=["Some string", 0, dt, False, d, None])
        expected_eson = '{"name": "Jane Doe", "log": {"__eson-list__": {"0": "Some string", "1": 0, "EsonDatetime~2": {"timestamp": 1588822240000400}, "3": false, "EsonDate~4": {"year": 2020, "month": 4, "day": 20}, "5": null}}}'
        self.assertEqual(expected_eson, eson.encode(data))

    def test_combined_list_data_decode(self):
        eson_string = '{"name": "Jane Doe", "log": {"__eson-list__": {"0": "Some string", "1": 0, "EsonDatetime~2": {"timestamp": 1588822240000400}, "3": false, "EsonDate~4": {"year": 2020, "month": 4, "day": 20}, "5": null}}}'
        d = date(year=2020, month=4, day=20)
        dt = datetime(year=2020, month=5, day=7, hour=6, minute=30, second=40, microsecond=400)
        expected_data = dict(name="Jane Doe", log=["Some string", 0, dt, False, d, None])
        self.assertEqual(expected_data, eson.decode(eson_string))


if __name__ == '__main__':
    unittest.main(verbosity=2, buffer=True)
