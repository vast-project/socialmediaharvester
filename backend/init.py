#!/usr/bin/env python3

from settings import DEBUG, MASTO_FILE, MASTO_APPNAME
from mastodon import Mastodon  # type: ignore

if __name__ == "__main__":
    if DEBUG:
        print(f"Secret file: {MASTO_FILE}")
    client_id, client_secret = Mastodon.create_app(
        MASTO_APPNAME,
        api_base_url="https://fediscience.org",
        to_file=MASTO_FILE
        # MASTO_APPNAME, api_base_url="https://qoto.org", to_file=MASTO_FILE
        # MASTO_APPNAME, api_base_url="https://masto.bg", to_file=MASTO_FILE
    )
    # print(client_id)
    # print(client_secret)
