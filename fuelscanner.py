#!/usr/bin/env python

from itertools import product
from operator import attrgetter
import feedparser


class Station(object):
    """Fuel Station summary object."""

    def __init__(self, name, address, price, discount=0):
        """Initiate Station object.

        Args:
            name (str): Business name of the fuel station.
            address (str): Address of the station.
            price (float): Fuel price in cents per litre.
            discount (int, optional): Discount of fuel in cents per litre.
        """
        self.name = name
        self.address = address
        self.price = price
        self.discount = discount

    def __eq__(self, other):
        """Equal iff all instance attributes equal."""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __str__(self):
        """Return summary of Station attributes."""
        head = f'{self.name} with a fuel price of {self.discount_price} c/L'
        tail = f'at {self.address}'

        if self.discount:
            mid = f'(incl. discount of {self.discount} c/L)'
            return ' '.join([head, mid, tail])
        return ' '.join([head, tail])

    @property
    def discount_price(self):
        """Fuel price with discount included."""
        return self.price - self.discount


def format_url(feed_url, suburbs):
    """Format URLs for the FuelWatch RSS feed."""
    if isinstance(suburbs, str):
        return '&Suburb='.join([feed_url, suburbs]),

    urls = tuple('&Suburb='.join(url) for url in product([feed_url], suburbs))
    return urls


def parse_feed(url_set, fuel_vouchers=None):
    """Parse the RSS feeds and return list of station summaries."""
    if not isinstance(fuel_vouchers, dict):
        fuel_vouchers = {'': 0}
    if isinstance(url_set, str):
        # Avoid iterating over string in the following loop.
        url_set = [url_set]

    station_summary_list = list()
    for url in url_set:
        rss_feed = feedparser.parse(url)
        for entry in rss_feed.entries:
            station = Station(
                name=entry.get('trading-name'),
                address=entry.address,
                price=float(entry.price),
                discount=fuel_vouchers.get(entry.brand, 0)
            )
            station_summary_list.append(station)
    return station_summary_list


def find_cheapest_station(stations):
    """Find the stations with the cheapest fuel price."""
    cheapest_station = min(stations, key=attrgetter('discount_price'))
    min_price = cheapest_station.discount_price
    return [s for s in stations if s.discount_price == min_price]


def main():
    """Script entry point."""
    # To-Do: Load data from CLI or ini file.
    suburbs = ['Scarborough', 'Cottesloe']
    fuelwatch_url = 'http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?'
    urls = format_url(fuelwatch_url, suburbs)
    stations = parse_feed(urls)
    cheapest_stations = find_cheapest_station(stations)

    print('The cheapest fuel stations:')
    for station in cheapest_stations:
        print(station)


if __name__ == "__main__":
    main()
