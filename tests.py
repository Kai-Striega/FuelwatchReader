import unittest
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


if __name__ == '__main__':
    unittest.main()
