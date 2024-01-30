#!/usr/bin/env python3
from typing import Dict

import logging

logger = logging.getLogger()

from settings import DEBUG, MASTO_FILE, TOKEN_FILE
from mastodon import Mastodon  # type: ignore


class MastodonEndpoint:
    def __init__(self, settings_map: Dict[str, str]):
        self.settings_map = settings_map

    def get_client(self) -> Mastodon:
        """Get Twitter API v2 interface"""
        print(self.settings_map)
        email = self.settings_map["email"]
        password = self.settings_map["password"]
        # bearer_token = self.settings_map["bearer_token"]
        # api_key = self.settings_map["api_key"]
        # api_key_secret = self.settings_map["api_key_secret"]
        # access_token = self.settings_map["access_token"]
        # access_token_secret = self.settings_map["access_token_secret"]
        # bearer_token=bearer_token,
        # consumer_key=api_key,
        # consumer_secret=api_key_secret,
        # access_token=access_token,
        # access_token_secret=access_token_secret,
        # mastodon = Mastodon(
        #     client_id=MASTO_APPNAME,
        # )

        mastodon = Mastodon(client_id=MASTO_FILE, debug_requests=DEBUG)
        mastodon.log_in(email, password, to_file=TOKEN_FILE)

        return mastodon
