"""Abstract interface for social networks.
Responsible to forward to social network, according to id"""

from settings import SOCIAL_NETWORK_CLASS
from . import persistence


def load_client(user: str, snet_id: int = 2):
    """Returns the relevant social media client"""
    mod_name, class_name = SOCIAL_NETWORK_CLASS.split(".")
    mod = __import__(f"sql_app.{mod_name}", fromlist=[class_name])
    socnet_client = getattr(mod, class_name)
    settings = persistence.get_settings(user)
    result = socnet_client(settings)
    assert result.sn_id == snet_id
    return result


def insert_all_pending_tweets(status: int, user: str, snet_id: int = 2):
    openconn = load_client(user)
    assert openconn.sn_id == snet_id
    return openconn.insert_all_pending_tweets(status=status, user=user)


def get_all_answer_post(post_id: int, user: str):
    openconn = load_client(user)
    return openconn.get_all_answer_post(post_id=post_id)


def get_poll_from_id(post_id: int, user: str):
    openconn = load_client(user)
    # if snet_id == 1:
    return openconn.get_poll_from_id(post_id=post_id)
    # else:
    # return None


def get_post_from_netid(id_on_snet: str, user: str, snet_id: int = 2):
    openconn = load_client(user, snet_id)
    return openconn.get_post_by_netid(id_on_snet, user)


# def get_all_quote_post(post: int, user: str, snet_id: int = 1):
#     settings = persistence.get_settings(user)
#     Tw_openconn = twitter_client.TwitterClient(settings)
#     Tw_openconn.get_all_quote_post(post_id=post)
#     return None


def get_aut_status(user: str, snet_id: int = 2):
    openconn = load_client(user)
    try:
        result = openconn.get_status()
    except Exception as e:
        result = {"error": str(e)}
    return result
