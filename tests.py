import unittest
import fuelscanner
from fuelscanner import Station


class TestFindCheapestStations(unittest.TestCase):

    def test_finds_cheapest_with_single_min(self):
        stations = [
            Station('Caltex Beckenham', '63 William St', 128.9, 0),
            Station('Caltex Bassendean', '309 Guild Rd', 129.9, 0)
        ]
        expected_cheapest_station = stations[0]
        cheapest_station = fuelscanner.find_cheapest_station(stations, 1)
        self.assertEqual([expected_cheapest_station], cheapest_station)

    def test_finds_cheapest_with_multiple_min(self):
        stations = [
            Station('Caltex Beckenham', '63 William St', 128.9, 0),
            Station('Caltex Bassendean', '309 Guild Rd', 128.9, 0),
            Station('Shell Gidgegannup', '2095 Toodyay Rd', 137.9, 0)
        ]
        expected_cheapest_stations = stations[:2]
        cheapest_stations = fuelscanner.find_cheapest_station(stations, 2)
        self.assertEqual(expected_cheapest_stations, cheapest_stations)


class TestUrlFormatter(unittest.TestCase):

    def test_urls_with_single_suburb(self):
        url = 'sample_url'
        suburb = 'SuburbA'
        excpected_url = ('sample_url&Suburb=SuburbA',)
        actual_url = fuelscanner.format_url(url, suburb)
        self.assertEqual(actual_url, excpected_url)

    def test_urls_with_two_suburbs(self):
        url = 'sample_url'
        suburbs = ('SuburbA', 'SuburbB')
        excpected_urls = (
            'sample_url&Suburb=SuburbA',
            'sample_url&Suburb=SuburbB'
        )
        actual_urls = fuelscanner.format_url(url, suburbs)
        self.assertEqual(actual_urls, excpected_urls)


class TestFeedParser(unittest.TestCase):

    def test_correct_station_returned_from_parser(self):
        actual_stations = fuelscanner.parse_feed('fixtures/testfeedone.xml')
        self.assertTrue(len(actual_stations) == 2)

        expected_stations = [
            Station('Caltex Beckenham', '63 William St', 128.9, 0),
            Station('Caltex Bassendean', '309 Guild Rd', 129.9, 0)
        ]
        self.assertEqual(expected_stations, actual_stations)
        station = Station('Vibe Mt Helena', '9 McVicar Pl', 126.9, 0)
        self.assertNotIn(station, actual_stations)

    def test_parses_correctly_given_multiple_feeds(self):
        test_urls = ('fixtures/testfeedone.xml', 'fixtures/testfeedtwo.xml')
        expected_stations = [
            Station('Caltex Beckenham', '63 William St', 128.9, 0),
            Station('Caltex Bassendean', '309 Guild Rd', 129.9, 0),
            Station('Shell Gidgegannup', '2095 Toodyay Rd', 137.9, 0)
        ]
        actual_stations = fuelscanner.parse_feed(test_urls)
        self.assertEqual(expected_stations, actual_stations)

        station = Station('Vibe Mt Helena', '9 McVicar Pl', 126.9, 0)
        self.assertNotIn(station, actual_stations)

    def test_applies_discount_while_parsing(self):
        test_vouchers = {'caltex': 5, 'some_other_voucher': 7}
        test_urls = ['fixtures/testfeedone.xml', 'fixtures/testfeedtwo.xml']
        expected_stations = [
            Station('Caltex Beckenham', '63 William St', 128.9, 5),
            Station('Caltex Bassendean', '309 Guild Rd', 129.9, 5),
            Station('Shell Gidgegannup', '2095 Toodyay Rd', 137.9, 0)
        ]
        actual_stations = fuelscanner.parse_feed(test_urls, test_vouchers)
        self.assertEqual(expected_stations, actual_stations)

    def test_ignores_poorly_formated_rss_feeds(self):
        test_urls = ['fixtures/testfeedtwo.xml', 'poorly_formatted_feed.xml']
        expected_station = [
            Station('Shell Gidgegannup', '2095 Toodyay Rd', 137.9, 0)
        ]
        actual_stations = fuelscanner.parse_feed(test_urls)
        self.assertEqual(expected_station, actual_stations)


if __name__ == '__main__':
    unittest.main()
