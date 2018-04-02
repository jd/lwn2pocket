#!/usr/bin/env python
import lwn2pocket
import pocket

request_token = pocket.Pocket.get_request_token(
    consumer_key=lwn2pocket.POCKET_CONSUMER_KEY,
    redirect_uri="http://localhost:8080/")
auth_url = pocket.Pocket.get_auth_url(
    code=request_token,
    redirect_uri="http://localhost:8080/")

print("Go to %s and press enter" % auth_url)
input()

user_credentials = pocket.Pocket.get_credentials(
    consumer_key=lwn2pocket.POCKET_CONSUMER_KEY,
    code=request_token)
access_token = user_credentials['access_token']

print("Access granted! Your token is: %s" % access_token)
