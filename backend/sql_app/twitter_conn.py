from typing import Dict

import tweepy  # type: ignore

import logging

logger = logging.getLogger()


class TwitterEndpoint:
    """Currently unaware of own Twitter handle"""

    s_network = 1
    """Twitter endpoints interface"""

    def __init__(self, settings_map: Dict[str, str]):
        self.settings_map = settings_map
        # self.api_key = settings_map["api_key"]
        # self.api_key_secret = settings_map["api_key_secret"]
        # self.access_token = settings_map["access_token"]
        # self.access_token_secret = settings_map["access_token_secret"]
        # self.bearer_token = settings_map["bearer_token"]
        # self.client_ID = settings_map["client_ID"]
        # self.client_secret = settings_map["client_Secret"]

    # def get_setting_value(self, key: str) -> str:
    #     if key not in self.settings_map:
    #         raise ValueError(f"No setting found with key {key}")
    #     return urllib.parse.unquote_plus(self.settings_map[key])

    def get_setting(self) -> tweepy.API:
        """Get Twitter API v1.1 interface"""
        api_key = self.settings_map["api_key"]
        api_key_secret = self.settings_map["api_key_secret"]
        access_token = self.settings_map["access_token"]
        access_token_secret = self.settings_map["access_token_secret"]

        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        try:
            api.verify_credentials()
            print("credenziali ok")
        except tweepy.errors.TweepyException as e:
            logger.error(f"Error verifying credentials: {str(e)}")
            raise e
        logger.info("API created")
        return api

    def get_client(self) -> tweepy.Client:
        """Get Twitter API v2 interface"""
        bearer_token = self.settings_map["bearer_token"]
        api_key = self.settings_map["api_key"]
        api_key_secret = self.settings_map["api_key_secret"]
        access_token = self.settings_map["access_token"]
        access_token_secret = self.settings_map["access_token_secret"]
        client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_key_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

        return client
