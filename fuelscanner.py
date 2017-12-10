#!/usr/bin/env python

from itertools import product

def format_url(feed_url, suburbs):
    """Format URLs for the FuelWatch RSS feed"""

    if isinstance(suburbs, str):
        return '&Suburb='.join([feed_url, suburbs]),

    urls = tuple('&Suburb='.join(url) for url in product([feed_url], suburbs))
    return urls
