import unittest
from fuelscanner import Station, format_url, parse_feed


class TestStationClass(unittest.TestCase):

    def test_discounted_price_property(self):
        station_1 = Station('Station 1', 'Address 1', 128.9, discount=4)
        self.assertEqual(station_1.discounted_price, 124.9)
        station_2 = Station('Station 2', 'Address 2', 125.0)
        self.assertEqual(station_2.discounted_price, 125.0)
        station_2.discount = 4
        self.assertEqual(station_2.discounted_price, 121.0)

    def test_station_equality(self):
        """Station attributes must all be equal for Station equality."""
        station_a = Station('Station 1', 'Address 1', 100)
        station_b = Station('Station 1', 'Address 1', 100)
        station_c = Station('Not Station 1', 'Address 1', 100)

        self.assertEqual(station_a, station_b)
        self.assertNotEqual(station_a, station_c)
        self.assertNotEqual(station_b, station_c)


class TestUrlFormatter(unittest.TestCase):

    def test_urls_with_single_suburb(self):
        url = 'sample_url'
        suburb = 'SuburbA'
        excpected_url = ('sample_url&Suburb=SuburbA',)
        actual_url = format_url(url, suburb)
        self.assertEqual(actual_url, excpected_url)

    def test_urls_with_two_suburbs(self):
        url = 'sample_url'
        suburbs = ('SuburbA', 'SuburbB')
        excpected_urls = (
            'sample_url&Suburb=SuburbA',
            'sample_url&Suburb=SuburbB'
        )
        actual_urls = format_url(url, suburbs)
        self.assertEqual(actual_urls, excpected_urls)


class TestFeedParser(unittest.TestCase):

    def test_correct_station_returned_from_parser(self):
        actual_stations = parse_feed('fixtures/testfeedone.xml')
        self.assertTrue(len(actual_stations) == 2)

        expected_stations = (
            Station('Caltex Beckenham', '63 William St', 128.9),
            Station('Caltex Bassendean', '309 Guildford Rd', 129.9)
        )

        for station in expected_stations:
            self.assertIn(station, actual_stations)

        un_expected_station = Station('Vibe Mt Helena', '9 McVicar Pl', 126.9)
        self.assertNotIn(un_expected_station, actual_stations)

    def test_parses_correctly_given_multiple_feeds(self):
        test_urls = ('fixtures/testfeedone.xml', 'fixtures/testfeedtwo.xml')
        actual_stations = parse_feed(test_urls)
        self.assertTrue(len(actual_stations) == 3)

        expected_stations = (
            Station('Caltex Beckenham', '63 William St', 128.9),
            Station('Caltex Bassendean', '309 Guildford Rd', 129.9),
            Station('Shell Gidgegannup', '2095 Toodyay Rd', 137.9)
        )
        for station in expected_stations:
            self.assertIn(station, actual_stations)

        un_expected_station = Station('Vibe Mt Helena', '9 McVicar Pl', 126.9)
        self.assertNotIn(un_expected_station, actual_stations)


if __name__ == '__main__':
    unittest.main()
