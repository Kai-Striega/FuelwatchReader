import unittest
import configparser
import os

import fuelscanner
from fuelscanner import Station

DIR_NAME = os.path.dirname(os.path.realpath(__file__))
TEST_URL_ONE = os.path.join(os.sep, DIR_NAME, 'fixtures', 'testfeedone.xml')
TEST_URL_TWO = os.path.join(os.sep, DIR_NAME, 'fixtures', 'testfeedtwo.xml')
TEST_CONFIG = os.path.join(os.sep, DIR_NAME, 'fixtures', 'test_configfile.ini')

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
        url = 'sample_url&'
        url_arguments = {'Suburb': ['SuburbA']}
        excpected_url = ['sample_url&Suburb=SuburbA']
        actual_url = fuelscanner.format_url(url, **url_arguments)
        self.assertEqual(actual_url, excpected_url)

    def test_urls_with_two_suburbs(self):
        url = 'sample_url&'
        url_arguments = {'Suburb': ['SuburbA', 'SuburbB']}
        excpected_urls = [
            'sample_url&Suburb=SuburbA',
            'sample_url&Suburb=SuburbB'
        ]
        actual_urls = fuelscanner.format_url(url, **url_arguments)
        self.assertEqual(actual_urls, excpected_urls)

    def test_returns_only_url_if_no_other_args_given(self):
        url = 'sample_url&'
        excpected_url = ['sample_url&']
        actual_url = fuelscanner.format_url(url)
        self.assertEqual(actual_url, excpected_url)

    def test_url_with_multiple_args(self):
        url = 'sample_url&'
        url_args = {
            'Suburb': ['SuburbA', 'SuburbB'],
            'Product': ['1', '2']
        }
        excpected_urls = [
            'sample_url&Suburb=SuburbA&Product=1',
            'sample_url&Suburb=SuburbB&Product=1',
            'sample_url&Suburb=SuburbA&Product=2',
            'sample_url&Suburb=SuburbB&Product=2'
        ]
        actual_urls = fuelscanner.format_url(url, **url_args)

        self.assertEqual(set(actual_urls), set(excpected_urls))


class TestFeedParser(unittest.TestCase):

    def test_correct_station_returned_from_parser(self):
        actual_stations = fuelscanner.parse_feed(TEST_URL_ONE)
        self.assertTrue(len(actual_stations) == 2)

        expected_stations = [
            Station('Caltex Beckenham', '63 William St', 128.9, 0),
            Station('Caltex Bassendean', '309 Guild Rd', 129.9, 0)
        ]
        self.assertEqual(expected_stations, actual_stations)
        station = Station('Vibe Mt Helena', '9 McVicar Pl', 126.9, 0)
        self.assertNotIn(station, actual_stations)

    def test_parses_correctly_given_multiple_feeds(self):
        test_urls = (TEST_URL_ONE, TEST_URL_TWO)
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
        test_urls = [TEST_URL_ONE,  TEST_URL_TWO]
        expected_stations = [
            Station('Caltex Beckenham', '63 William St', 128.9, 5),
            Station('Caltex Bassendean', '309 Guild Rd', 129.9, 5),
            Station('Shell Gidgegannup', '2095 Toodyay Rd', 137.9, 0)
        ]
        actual_stations = fuelscanner.parse_feed(test_urls, test_vouchers)
        self.assertEqual(expected_stations, actual_stations)

    def test_ignores_poorly_formated_rss_feeds(self):
        test_urls = [TEST_URL_TWO, 'poorly_formatted_feed.xml']
        expected_station = [
            Station('Shell Gidgegannup', '2095 Toodyay Rd', 137.9, 0)
        ]
        actual_stations = fuelscanner.parse_feed(test_urls)
        self.assertEqual(expected_station, actual_stations)


class TestMessageFormattingAndSending(unittest.TestCase):

    def test_message_formats_single_station(self):
        fuel_station = Station('Caltex Beckenham', '63 William St', 128.9, 5)

        expected_message = '\n'.join([
            'The cheapest fuel stations:',
            '128.9 (5) at Caltex Beckenham, 63 William St'
        ])

        message = fuelscanner.format_message([fuel_station])
        self.assertEqual(message, expected_message)

    def test_formats_multiple_stations(self):
        fuel_stations = [
            Station('Caltex Beckenham', '63 William St', 128.9, 5),
            Station('Shell Gidgegannup', '2095 Toodyay Rd', 137.9, 0)
        ]

        expected_message = '\n'.join([
            'The cheapest fuel stations:',
            '128.9 (5) at Caltex Beckenham, 63 William St',
            '137.9 (0) at Shell Gidgegannup, 2095 Toodyay Rd'
        ])

        message = fuelscanner.format_message(fuel_stations)
        self.assertEqual(message, expected_message)

    def test_sends_sms_message(self):
        config = configparser.ConfigParser()
        config.read(TEST_CONFIG)

        message = 'This is a simple test message'
        if config['TWILIO'].getboolean('trial_account'):
            message = 'Sent from your Twilio trial account - ' + message

        returned_message = fuelscanner.send_sms_message(
            message,
            config['TWILIO']['test_sid'],
            config['TWILIO']['test_auth_token'],
            config['TWILIO']['mobile_number'],
            config['TWILIO']['twilio_number']
        )
        self.assertEqual(message, returned_message.body)


if __name__ == '__main__':
    unittest.main()
