#!/usr/bin/env python
""" twitch_channels.py - Queries Twitch for channels of interest.
    Used in conjunction with livestreamer-completion.

    Usage examples:

      ./twitch_channels.py --follows myname
      ./twitch_channels.py --team eg --team teamliquid

"""

from __future__ import print_function

from argparse import ArgumentParser
from functools import partial
from itertools import chain

import requests


API_BASE_URL = "api.twitch.tv"

def api(path, *args, **params):
    insecure = params.pop("insecure", False)
    proto = insecure and "http://" or "https://"
    url = proto + API_BASE_URL + path.format(*args)
    res = requests.get(url, params=params)

    return res.json()


def page_result(res):
    for key, values in res.items():
        if not key.startswith("_"):
            return values

    return []


def iterate_pages(func, limit=25):
    offset, total = 0, limit

    while offset < total:
        res = func(limit=limit, offset=offset)
        values = page_result(res)

        offset += len(values)
        total = res.get("_total")

        yield values


def iterate_pages_result(*args, **kwargs):
    return chain.from_iterable(iterate_pages(*args, **kwargs))


def print_channels(channels):
    for channel in channels:
        channel_name = channel.get("channel").get("name")
        print("twitch.tv/{0}".format(channel_name))


# Twitch APIs
team_channels = partial(api, "/api/team/{0}/all_channels.json", insecure=True)
streams = partial(api, "/kraken/streams")
user_follows = partial(api, "/kraken/users/{0}/follows/channels")


parser = ArgumentParser()
parser.add_argument("-f", "--follows", action="append", default=[],
                    metavar="user", help="channels a user is following",)
parser.add_argument("-t", "--team", action="append", default=[],
                    metavar="team", help="channels that are part of a team")
parser.add_argument("-o", "--online", action="store_true",
                    help="Only return the channels that are online")


def main():
    args = parser.parse_args()
    if not (args.follows or args.team):
        return parser.print_help()

    channels = []
    for user in args.follows:
        myuser_follows = partial(user_follows, user)
        channels += iterate_pages_result(myuser_follows, limit=100)

    for team in args.team:
        channels += team_channels(team).get("channels", [])

    if args.online:
        channel_list = ",".join(c.get("channel").get("name") for c in channels)
        online_channels = streams(channel=channel_list).get("streams")
        if online_channels:
            print_channels(online_channels)
    else:
        print_channels(channels)


if __name__ == "__main__":
    main()

