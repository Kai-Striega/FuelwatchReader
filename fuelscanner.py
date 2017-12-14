#!/usr/bin/env python

from itertools import product
import feedparser


class Station(object):
    """Fuel Station summary object."""

    def __init__(self, name, address, price, discount=0):
        """Instantiate Station object.

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
        """Override default Equals behaviour."""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    @property
    def discounted_price(self):
        """Fuel price with discount included."""
        return self.price - self.discount


def format_url(feed_url, suburbs):
    """Format URLs for the FuelWatch RSS feed."""
    if isinstance(suburbs, str):
        return '&Suburb='.join([feed_url, suburbs]),

    urls = tuple('&Suburb='.join(url) for url in product([feed_url], suburbs))
    return urls


def parse_feed(url_set):
    """Parse the RSS feeds and return list of station summaries."""
    if isinstance(url_set, str):
        url_set = [url_set]

    station_summary_list = list()
    for url in url_set:
        rss_feed = feedparser.parse(url)
        for entry in rss_feed.entries:
            station = Station(
                name=entry.get('trading-name'),
                address=entry.get('address'),
                price=float(entry.get('price'))
            )
            station_summary_list.append(station)
    return station_summary_list
