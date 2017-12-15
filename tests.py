import unittest
import fuelscanner


class TestStationClass(unittest.TestCase):

    def test_discounted_price_property(self):
        station_1 = fuelscanner.Station('Station 1', 'Address 1', 128.9, 4)
        self.assertEqual(station_1.discounted_price, 124.9)
        station_2 = fuelscanner.Station('Station 2', 'Address 2', 125.0)
        self.assertEqual(station_2.discounted_price, 125.0)
        station_2.discount = 4
        self.assertEqual(station_2.discounted_price, 121.0)

    def test_station_equality(self):
        """Station attributes must all be equal for Station equality."""
        station_a = fuelscanner.Station('Station A', 'Address 1', 100)
        station_b = fuelscanner.Station('Station A', 'Address 1', 100)
        station_c = fuelscanner.Station('Not Station A', 'Address 1', 100)

        self.assertEqual(station_a, station_b)
        self.assertNotEqual(station_a, station_c)
        self.assertNotEqual(station_b, station_c)

    def test_station_string_magic_method(self):
        station_a = fuelscanner.Station('Station A', 'Address 1', 100)
        expected_string = 'Station A with a fuel price of 100 c/L at Address 1'
        actual_string = str(station_a)
        self.assertEqual(expected_string, actual_string)

        station_a.discount = 4
        expected_string_discount = 'Station A with a fuel price of 96 c/L\
 (incl. discount of 4 c/L) at Address 1'
        actual_string_discount = str(station_a)
        self.assertEqual(expected_string_discount, actual_string_discount)


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
            fuelscanner.Station('Caltex Beckenham', '63 William St', 128.9),
            fuelscanner.Station('Caltex Bassendean', '309 Guild Rd', 129.9)
        ]
        self.assertEqual(expected_stations, actual_stations)
        station = fuelscanner.Station('Vibe Mt Helena', '9 McVicar Pl', 126.9)
        self.assertNotIn(station, actual_stations)

    def test_parses_correctly_given_multiple_feeds(self):
        test_urls = ('fixtures/testfeedone.xml', 'fixtures/testfeedtwo.xml')
        expected_stations = [
            fuelscanner.Station('Caltex Beckenham', '63 William St', 128.9),
            fuelscanner.Station('Caltex Bassendean', '309 Guild Rd', 129.9),
            fuelscanner.Station('Shell Gidgegannup', '2095 Toodyay Rd', 137.9)
        ]
        actual_stations = fuelscanner.parse_feed(test_urls)
        self.assertEqual(expected_stations, actual_stations)

        station = fuelscanner.Station('Vibe Mt Helena', '9 McVicar Pl', 126.9)
        self.assertNotIn(station, actual_stations)

    def test_applies_discount_while_parsing(self):
        test_vouchers = {'Caltex': 5, 'some_other_voucher': 7}
        test_urls = ['fixtures/testfeedone.xml', 'fixtures/testfeedtwo.xml']
        expected_stations = [
            fuelscanner.Station('Caltex Beckenham', '63 William St', 128.9, 5),
            fuelscanner.Station('Caltex Bassendean', '309 Guild Rd', 129.9, 5),
            fuelscanner.Station('Shell Gidgegannup', '2095 Toodyay Rd', 137.9)
        ]
        actual_stations = fuelscanner.parse_feed(test_urls, test_vouchers)
        self.assertEqual(expected_stations, actual_stations)

    def test_ignores_poorly_formated_rss_feeds(self):
        test_urls = ['fixtures/testfeedtwo.xml', 'poorly_formatted_feed.xml']
        expected_station = [
            fuelscanner.Station('Shell Gidgegannup', '2095 Toodyay Rd', 137.9)
        ]
        actual_stations = fuelscanner.parse_feed(test_urls)
        self.assertEqual(expected_station, actual_stations)

if __name__ == '__main__':
    unittest.main()
