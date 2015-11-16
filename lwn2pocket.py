#!/usr/bin/env python
import logging
import netrc
import os
import re

import pocket
import requests


logging.basicConfig()
LOG = logging.getLogger(__name__)

DEBUG = False
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


def get_login_password(site_name="lwn.net", netrc_file="~/.netrc"):
    """Read a .netrc file and return login/password for LWN."""
    n = netrc.netrc(os.path.expanduser(netrc_file))
    return n.hosts[site_name][0], n.hosts[site_name][2]


def get_login_cookies():
    """Login into LWN.net and returns the cookies."""
    username, password = get_login_password()
    return requests.post("https://lwn.net/login",
                         allow_redirects=False,
                         data={"Username": username,
                               "Password": password}).cookies

RE_SUBSCRIBER_LINK_FORM = re.compile(
    "<input type=\"hidden\" name=\"articleid\" value=\"(\d+)\">")

RE_SUBSCRIBER_LINK = re.compile("http://lwn.net/SubscriberLink/(\d+)/.+/")


def main():
    cookies = get_login_cookies()

    bigpage = requests.get("https://lwn.net/current/bigpage",
                           cookies=cookies)

    _, access_token = get_login_password("pocket.com")
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
            link = requests.post("https://lwn.net/SubscriberLink/MakeLink",
                                 data={"articleid": articleid},
                                 cookies=cookies)
            RE_SUBLINK = re.compile(
                "<a href=\"(http://lwn.net/SubscriberLink/%s/.+)\">"
                % articleid)
            for line in link.text.split("\n"):
                m = RE_SUBLINK.search(line)
                if m:
                    p.add(m.group(1))
                    break

if __name__ == '__main__':
    main()
