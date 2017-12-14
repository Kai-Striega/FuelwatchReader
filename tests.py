import unittest
from collections import namedtuple
import fuelscanner
from fuelscanner import Station


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

    def setUp(self):
        self.expected_station_1 = Station(
            name='Caltex Woolworths Beckenham',
            address='63 William St',
            brand='Caltex Woolworths',
            price=128.9
        )
        self.expected_station_2 = Station(
            name='Caltex StarMart Bassendean',
            address='309 Guildford Rd (Cnr North Rd)',
            brand='Caltex',
            price=129.9
        )
        self.expected_station_3 = Station(
            name='Shell Gidgegannup',
            address='2095 Toodyay Rd',
            brand='Shell',
            price=137.9
        )
        self.un_expected_station = Station(
            name='Vibe Mt Helena',
            address='9 McVicar Pl',
            brand='Vibe',
            price=126.9
        )

    def test_correct_station_returned_from_parser(self):
        actual_stations = fuelscanner.parse_feed('fixtures/testfeedone.xml')

        self.assertTrue(len(actual_stations) == 2)
        self.assertIn(self.expected_station_1, actual_stations)
        self.assertIn(self.expected_station_2, actual_stations)
        self.assertNotIn(self.un_expected_station, actual_stations)

    def test_parses_correctly_given_multiple_feeds(self):
        test_urls = ('fixtures/testfeedone.xml', 'fixtures/testfeedtwo.xml')
        actual_stations = fuelscanner.parse_feed(test_urls)

        self.assertTrue(len(actual_stations) == 3)
        self.assertIn(self.expected_station_1, actual_stations)
        self.assertIn(self.expected_station_2, actual_stations)
        self.assertIn(self.expected_station_3, actual_stations)
        self.assertNotIn(self.un_expected_station, actual_stations)

if __name__ == '__main__':
    unittest.main()
