#!/usr/bin/env python
import logging
import os
import re
import sys

import pocket
import requests


logging.basicConfig()
LOG = logging.getLogger(__name__)

DEBUG = len(sys.argv) >= 2 and sys.argv[1] == '--debug'
POCKET_CONSUMER_KEY = "44549-fa6a1b90e0b637237765ba8a"


if DEBUG:
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


RE_SUBSCRIBER_LINK_FORM = re.compile(
    "<input type=\"hidden\" name=\"articleid\" value=\"(\d+)\">")

RE_SUBSCRIBER_LINK = re.compile("https://lwn.net/SubscriberLink/(\d+)/.+/")


def main():
    session = requests.Session()
    session.post(
        "https://lwn.net/Login/",
        data={"Username": os.getenv("LWNNET_USERNAME"),
              "Password": os.getenv("LWNNET_PASSWORD")}).cookies

    bigpage = session.get("https://lwn.net/current/bigpage")

    access_token = os.getenv("POCKET_ACCESS_TOKEN")
    p = pocket.Pocket(POCKET_CONSUMER_KEY, access_token)

    already_in_pocket = p.get(domain="lwn.net", detailType="simple",
                              state="all")
    articles_already_pushed = set()
    if already_in_pocket[0]['list']:
        for entry_id, entry in already_in_pocket[0]['list'].items():
            m = RE_SUBSCRIBER_LINK.match(entry['given_url'])
            if m:
                articles_already_pushed.add(m.group(1))

    for line in bigpage.text.split("\n"):
        m = RE_SUBSCRIBER_LINK_FORM.search(line)
        if m:
            articleid = m.group(1)
            if articleid in articles_already_pushed:
                continue
            link = session.post("https://lwn.net/SubscriberLink/MakeLink",
                                data={"articleid": articleid})
            RE_SUBLINK = re.compile(
                "<a href=\"(https://lwn.net/SubscriberLink/%s/.+)\">"
                % articleid)
            for line in link.text.split("\n"):
                m = RE_SUBLINK.search(line)
                if m:
                    p.add(m.group(1))
                    break

if __name__ == '__main__':
    main()
