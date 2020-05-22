import unittest
import eson
import json
from datetime import datetime, date, timezone, timedelta


class TestCase(unittest.TestCase):
    def test_simple_encode(self):
        normal_dict = dict(name="Jane Doe", sibling="Jane Doe")
        self.assertEqual(json.dumps(normal_dict), eson.encode(normal_dict))
        self.assertEqual(eson.encode(None), 'null')

    def test_simple_decode(self):
        json_data = '{"name": "Jane Doe"}'
        self.assertEqual(eson.decode(json_data), dict(name="Jane Doe"))
        self.assertIsNone(eson.decode('null'))

    def test_list_encode(self):
        a_list = [1, 2, 3]
        expected_eson = '[1, 2, 3]'
        self.assertEqual(eson.encode(a_list), expected_eson)

    def test_list_decode(self):
        eson_data = '[1, 2, 3, "Some String"]'
        expected_list = [1, 2, 3, "Some String"]
        self.assertEqual(eson.decode(eson_data), expected_list)

    def test_date_encode(self):
        dob = date(year=2020, month=4, day=20)
        # Stand alone date
        self.assertEqual(eson.encode(dob), '{"EsonDate~": {"year": 2020, "month": 4, "day": 20}}')

        # Date in a dict
        data = dict(dob=dob, name="Corona")
        expected_eson = '{"EsonDate~dob": {"year": 2020, "month": 4, "day": 20}, "name": "Corona"}'
        self.assertEqual(eson.encode(data), expected_eson)

    def test_date_decode(self):
        # Stand alone date
        expected_date = date(year=1969, month=4, day=20)
        eson_date = '{"EsonDate~": {"year": 1969, "month": 4, "day": 20}}'
        self.assertEqual(eson.decode(eson_date), expected_date)
        # Dae in a dict
        eson_data = '{"EsonDate~dob": {"year": 1969, "month": 4, "day": 20}, "height": 30}'
        expected_data = dict(dob=expected_date, height=30)
        self.assertEqual(eson.decode(eson_data), expected_data)

    def test_datetime_encode(self):
        dt = datetime(year=2020, month=5, day=7, hour=6, minute=30, second=40, microsecond=400)
        data = dict(registered=dt, username="bear")
        expected_ts = int(dt.timestamp() * 1000000)
        expected_eson = '{"EsonDatetime~registered": {"timestamp": %d}, "username": "bear"}' % expected_ts
        self.assertEqual(eson.encode(data), expected_eson)

    def test_datetime_decode(self):
        dt = datetime.fromtimestamp(1588822240.0004)
        eson_data = '{"EsonDatetime~date_of_birth": {"timestamp": 1588822240000400}, "horoscope": "taurus"}'
        self.assertEqual(dict(date_of_birth=dt, horoscope="taurus"), eson.decode(eson_data))
    
    def test_combined_list_data_encode(self):
        d = date(year=2020, month=4, day=20)
        dt = datetime(year=2020, month=5, day=7, hour=6, minute=30, second=40, microsecond=400)
        data = dict(name="Jane Doe", log=["Some string", 0, dt, False, d, None])
        expected_ts = int(dt.timestamp() * 1000000)
        expected_eson = '{"name": "Jane Doe", "log": ["Some string", 0, {"EsonDatetime~": {"timestamp": %d}}, false, {"EsonDate~": {"year": 2020, "month": 4, "day": 20}}, null]}' % expected_ts
        self.assertEqual(expected_eson, eson.encode(data))

    def test_combined_list_data_decode(self):
        eson_string = '{"name": "Jane Doe", "log": ["Some string", 0, {"EsonDatetime~": {"timestamp": 1588822240000400}}, false, {"EsonDate~": {"year": 2020, "month": 4, "day": 20}}, null]}'
        d = date(year=2020, month=4, day=20)
        dt = datetime.fromtimestamp(1588822240.0004)
        expected_data = dict(name="Jane Doe", log=["Some string", 0, dt, False, d, None])
        self.assertEqual(expected_data, eson.decode(eson_string))

    def test_pretty_encoding(self):
        data = dict(name="Jane Doe", registered=date(year=2020, month=5, day=6))
        eson_data = {
            "name": "Jane Doe",
            "EsonDate~registered": dict(year=2020, month=5, day=6)
        }
        self.assertEqual(eson.encode(data, pretty=True), json.dumps(eson_data, indent=4))


if __name__ == '__main__':
    unittest.main(verbosity=2, buffer=True)
