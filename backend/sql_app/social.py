"""Abstract interface for social networks.
Responsible to forward to social network, according to id"""
from typing import List

import json

from . import twitter_client, persistence, media

# verifico e setto accessi a twitter
# Tw_openconn=twitter_client.TwitterClient(db=SessionLocal(),network='twitter',twuser='B_MCristina')

# nelle funzioni verrà chiamata il file twitter_client o crud_facebook (attualmente non esiste)
# in base al social su cui si verranno fatte le operazioni


def insert_all_pending_tweets(status: int, user: str, snet_id: int = 1):
    settings = persistence.get_settings(user)
    Tw_openconn = twitter_client.TwitterClient(settings)
    if snet_id == 0:
        list = []
        list.append(Tw_openconn.insert_all_pending_tweets(status=status, user=user))
        # list.append('None') #qua ci saranno i post di facebook
        return list
    elif snet_id == 1:
        return Tw_openconn.insert_all_pending_tweets(status=status, user=user)
    else:
        # da gestire i post di facebook
        return None


def get_all_answer_post(tweetid: int, user: str, snet_id: int = 1):
    settings = persistence.get_settings(user)
    Tw_openconn = twitter_client.TwitterClient(settings)
    if snet_id == 1:
        return Tw_openconn.get_all_answer_post(idpost=tweetid)
    else:
        return None


def get_poll_from_id(tweetid: int, user: str, snet_id: int = 1):
    settings = persistence.get_settings(user)
    Tw_openconn = twitter_client.TwitterClient(settings)
    # if snet_id == 1:
    return Tw_openconn.get_poll_from_id(post=tweetid)
    # else:
    # return None


def get_post_from_netid(id_on_snet: str, user: str, snet_id: int = 1):
    settings = persistence.get_settings(user)
    Tw_openconn = twitter_client.TwitterClient(settings)
    data = Tw_openconn.get_post_by_netid(id_on_snet)

    content_text = data[0]["text"]
    if not content_text:
        content_text = data[0]["tweets"][0]["text"]
    content = {"type": "post", "content": {"text": content_text}}

    image_files = []
    if data.includes and "media" in data.includes:
        for m in data.includes["media"]:
            fname = f'{m["media_key"]}-{m["url"].split("/")[-1]}'
            image_files += [media.download(m["url"], fname)]
    publ_date = data[0]["created_at"].date()

    if data.includes and "polls" in data.includes:
        options: List[str] = [o["label"] for o in data.includes["polls"][0]["options"]]
        content["content"]["poll_options"] = options  # type: ignore
        content["type"] = "poll"
        # TODO: duration seems to be missing

    return persistence.reflect_post_social_user(
        id_on_snet, json.dumps(content), image_files, publ_date, user
    )


# def get_all_quote_post(post: int, user: str, snet_id: int = 1):
#     settings = persistence.get_settings(user)
#     Tw_openconn = twitter_client.TwitterClient(settings)
#     Tw_openconn.get_all_quote_post(post_id=post)
#     return None


def get_aut_status(user: str, snet_id: int = 1):
    settings = persistence.get_settings(user)
    Tw_openconn = twitter_client.TwitterClient(settings)
    try:
        result = Tw_openconn.get_status()
    except Exception as e:
        result = {"error": str(e)}
    return result
