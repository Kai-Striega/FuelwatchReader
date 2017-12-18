#!/usr/bin/env python

import configparser
from itertools import product
from collections import namedtuple
import feedparser
from twilio.rest import Client

FUELWATCH_URL = 'http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?'
Station = namedtuple('Station', 'name address price discount')


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

    suburbs = config['USER DETAILS']['suburbs'].split(',')
    fuel_vouchers = dict(config['FUEL VOUCHERS'])

    urls = format_url(FUELWATCH_URL, suburbs)
    stations = parse_feed(urls, fuel_vouchers)
    cheapest_stations = find_cheapest_station(stations)

    message = format_message(cheapest_stations)

    twilio_sid = config['TWILIO']['sid']
    twilio_auth_token = config['TWILIO']['auth_token']
    twilio_number = config['TWILIO']['twilio_number']

    user_number = config['USER DETAILS']['mobile_number']

    send_sms_message(
        message,
        twilio_sid,
        twilio_auth_token,
        user_number,
        twilio_number
    )


if __name__ == "__main__":
    main()
