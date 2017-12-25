#!/usr/bin/env python

import configparser
from itertools import product
from collections import namedtuple, defaultdict
import feedparser
from twilio.rest import Client

FUELWATCH_URL = 'http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?'
Station = namedtuple('Station', 'name address price discount')


def parse_fuelwatch_params(config):
    """Return dict of lists of Fuelwatch parameters."""
    fuelwatch_param_fields = ('Suburb', 'Product', 'Day', 'Surrounding')
    fuelwatch_params = defaultdict(list)

    for field in fuelwatch_param_fields:
        parameter = config['FUELWATCH PARAMS'][field]
        if parameter:
            fuelwatch_params[field] = parameter.split(',')

    return fuelwatch_params


def format_url(feed_url, **kwargs):
    """Format URLs for the FuelWatch RSS feed."""
    pairs = (product([key.title()], value) for (key, value) in kwargs.items())
    joined_pairs = (map('='.join, pair) for pair in pairs)
    urls = [feed_url + '&'.join(args) for args in product(*joined_pairs)]
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
                discount=float(fuel_vouchers.get(entry.brand.lower(), 0))
            )
            station_summary_list.append(station)
    return station_summary_list


def find_cheapest_station(stations, n=2):
    """Find the stations with the cheapest fuel price."""
    cheapest_stations = sorted(stations, key=lambda x: x.price - x.discount)
    return cheapest_stations[:n]


def format_message(stations):
    """Return formatted message for end user."""
    message = ['The cheapest fuel stations:']
    for station in stations:
        message.append(
            f'{station.price} ({station.discount}) at {station.name}, {station.address}'
        )
    return '\n'.join(message)


def send_sms_message(body, sid, auth_token, user_number, twilio_number):
    """Send a text message to the user with the lowest fuel price."""
    client = Client(sid, auth_token)
    message = client.messages.create(
        to=user_number,
        from_=twilio_number,
        body=body)
    return message


def main():
    """Script entry point."""
    config = configparser.ConfigParser()
    config.read('configfile.ini')

    fuelwatch_params = parse_fuelwatch_params(config)
    urls = format_url(FUELWATCH_URL, **fuelwatch_params)

    fuel_vouchers = dict(config['FUEL VOUCHERS'])
    stations = parse_feed(urls, fuel_vouchers)
    cheapest_stations = find_cheapest_station(stations)
    message = format_message(cheapest_stations)

    twilio_sid = config['TWILIO']['sid']
    twilio_auth_token = config['TWILIO']['auth_token']
    twilio_number = config['TWILIO']['twilio_number']

    user_number = config['TWILIO']['mobile_number']

    send_sms_message(
        message,
        twilio_sid,
        twilio_auth_token,
        user_number,
        twilio_number
    )


if __name__ == "__main__":
    main()
