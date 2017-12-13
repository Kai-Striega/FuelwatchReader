import unittest
from collections import namedtuple
import fuelscanner


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

    def test_correct_station_are_returned_from_feed_parser(self):
        Station = namedtuple('Station', 'name address brand price')
        expected_station_1 = Station(
            name='Caltex Woolworths Beckenham',
            address='63 William St, BECKENHAM',
            brand='Caltex Woolworths',
            price=128.9
        )
        expected_station_2 = Station(
            name='Caltex StarMart Bassendean',
            address='309 Guildford Rd (Cnr North Rd), BASSENDEAN',
            brand='Caltex',
            price=129.9
        )
        expected_station_3 = Station(
            name='Shell Gidgegannup',
            address='2095 Toodyay Rd, GIDGEGANNUP',
            brand='Shell',
            price=137.9
        )
        un_expected_station = Station(
            name='Vibe Mt Helena',
            address='9 McVicar Pl',
            brand='Vibe',
            price=126.9
        )

        actual_stations = fuelscanner.parse_feed('fixtures/testfeedone.xml')

        self.assertIn(expected_station_1, actual_stations)
        self.assertIn(expected_station_2, actual_stations)
        self.assertIn(expected_station_3, actual_stations)
        self.assertNotIn(un_expected_station, actual_stations)


if __name__ == '__main__':
    unittest.main()