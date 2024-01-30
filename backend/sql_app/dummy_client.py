from typing import Dict

import json
from datetime import datetime

from settings import DEBUG
from util import urlencode, urldecode

from .abstract_client import AbstractClient
from .database import SessionLocal
from . import persistence, models

import logging

logger = logging.getLogger()


class DummyClient(AbstractClient):
    sn_name = "DUMMY"
    sn_id = 0

    def __init__(self, settings_map: Dict[str, str]):
        pass

    def insert_tweets(self, status: int, conten_str: str, idpost: int):
        list_res = []
        # devo cercare le immagini se ci sono e se sono legate al post
        # print(new_tweet)

        recordObject = {
            "status": "success",
            "post": [
                {
                    "post_id": idpost,
                    "post_on_network_id": 0,
                    "network": "mastodon",
                }
            ],
        }

        list_res.append(recordObject)
        # print(list_res)
        # se ho id vuol dire che il messaggio è stato inviato
        # allora faccio aggiornamento dello stato e id_on_network del post
        # id_on_network da salvare sul db
        persistence.update_post_status_id_on_network(
            idpost=idpost,
            status=status + 1,
            id_on_net=0,
            s_network=self.sn_id,
        )

        return list_res

    # creazione nuovo post di tipo poll su tw e sul db
    def insert_poll(
        self, idpost: int, status: int, list_opt, text_poll: str, duration_minutes: int
    ):
        # ricordare: You can only provide one of poll or media
        # newpoll = []
        # try:
        #     newpoll = self.client.make_poll(
        #         options=list_opt,
        #         # text=text_poll,
        #         expires_in=duration_minutes,
        #         # user_auth=True,
        #     )
        # except MastodonError as e:
        #     return {"error": str(e)}
        # try:
        #     new_tweet = self.client.status_post(
        #         text_poll, visibility=visibility, poll=newpoll
        #     )
        # except MastodonError as e:
        #     return {"error": str(e)}

        list_res = []
        # recupero i dati che devo inserire nel db
        id_on_tweet = 0

        persistence.update_post_status_id_on_network(
            idpost=idpost,
            status=status + 1,
            id_on_net=id_on_tweet,
            s_network=self.sn_id,
        )

        recordObject = {
            "status": "success",
            "post": [
                {
                    "post_id": idpost,
                    "post_on_network_id": id_on_tweet,
                    "network": "mastodon",
                }
            ],
        }
        list_res.append(recordObject)
        return list_res

    def status_retweeted(self, id_on_net):
        # the ID of the status
        # try:
        #     status = self.api.status_reblogged_by(id)
        # except MastodonError as e:
        #     return {"error": str(e)}
        retweet_count = 0
        print(
            "The number of time the status has been retweeted is : "
            + str(retweet_count)
        )

    def get_all_answer_post(self, idpost: int, delall: bool = True):
        # 1)cancello tutte le risposte salvate e le riscarico da zero
        # 1) del answer post x
        if delall:
            persistence.delete_answer(idpost)

        # 2)scarico tutte le risposte e le salvo nel db
        tweetid = (
            SessionLocal()
            .query(models.Post.id_on_network)
            .filter_by(id=idpost)
            .scalar()
        )
        print(tweetid)
        # try:
        #     t = self.client.status(tweetid)
        # except MastodonError as e:
        #     return {"error": str(e)}
        user_name = "dummy_user"
        print(user_name)
        replies = []
        # user_name = user #nome senza @
        # try:
        #     stw = self.client.status_context(tweetid)["decendants"]
        # except MastodonError as e:
        #     return {"error": str(e)}
        # for tweet in stw:
        #     # if hasattr(tweet, "in_reply_to_status_id_str"):
        #         # if tweet.in_reply_to_status_id_str == str(tweetid):
        #             # salvo nel db le risposte al tweetp
        #             dta_created_at = tweet["created_at"]

        #             content_text = tweet["content"]
        #             # content_text=urllib.parse.quote_plus(tweet.full_text)
        #             tweet_data = persistence.insert_answer_post(
        #                 idpost=idpost,
        #                 content=content_text,
        #                 author=tweet["account"]["screen_name"],
        #                 id_on_network=tweet["id"],
        #                 publication_date=dta_created_at,
        #                 reply_to=None,
        #             )
        #             # devo verificare se ci sono risposte a risposte
        #             self.get_all_answer_post_in_reply_to(
        #                 postid=idpost, tweetid=tweet["id"], user=tweet["account"]["screen_name"]
        #             )

        # 3)faccio un get dal db delle risposta al posto
        # dopo aver inserito tutte le risposte nel db devo restituirele interrogando direttamente il db
        self.get_all_retweet_post(tweetid, post=idpost)
        replies = persistence.get_answer_post(idpost=idpost)
        replies_all = []
        for r in replies:
            tdata = {
                "posts": [
                    {
                        "post_id": str(idpost),
                        "network": "mastodon",
                        "responses": [
                            {
                                "response_id": r.id,
                                "content": urldecode(r.content),
                                "children": r.reply_to,
                                "user_response_name": r.author,
                            }
                        ],
                    }
                ]
            }
            replies_all.append(tdata)
        return replies_all

    # get reply to answer (risposta a risposta)
    def get_all_answer_post_in_reply_to(self, postid: int, tweetid, user: str):
        user_name = user  # nome senza @
        # try:
        #     stw = self.client.status_context(tweetid)["decendants"]
        # except MastodonError as e:
        #     return {"error": str(e)}

        # for tweet in stw:
        #     # if hasattr(tweet, "in_reply_to_status_id_str"):
        #     #     if tweet.in_reply_to_status_id_str == str(tweetid):
        #             print("risposta:")
        #             # pp.pprint(tweet.__dict__)
        #             print(tweet["account"]["screen_name"])
        #             dta_created_at = tweet["created_at"]
        #             content_text = tweet["content"]
        #             # content_text=urllib.parse.quote_plus(tweet.full_text)
        #             tweet_data = persistence.insert_answer_post(
        #                 idpost=postid,
        #                 content=content_text,
        #                 author=tweet["account"]["screen_name"],
        #                 id_on_network=tweet["id"],
        #                 publication_date=dta_created_at,
        #                 reply_to=tweetid,
        #             )

        return None

    # get poll by id tweet
    def get_poll_from_id(self, post: int):
        persistence.delete_answer(idpost=post)
        tweetid = (
            SessionLocal().query(models.Post.id_on_network).filter_by(id=post).scalar()
        )
        # try:
        #     res_tweet = self.client.get_tweets(
        #         tweetid,
        #         expansions=["attachments.poll_ids", "author_id"],
        #         poll_fields=["duration_minutes", "end_datetime", "voting_status"],
        #     )
        # except MastodonError as e:
        #     return {"error": str(e)}
        res = {
            "polls": [
                {
                    "duration_minutes": 0,
                    "end_datetime": 0,
                    "voting_status": 0,
                    "options": [
                        {"votes": 0, "label": "1"},
                        {"votes": 0, "label": "2"},
                        {"votes": 0, "label": "3"},
                        {"votes": 0, "label": "4"},
                    ],
                }
            ]
        }

        try:
            res["polls"][0]
        except KeyError:
            raise TypeError("Provided tweet does not contain a poll!")

        poll = res["polls"][0]  # print (res)
        duration = poll["duration_minutes"]
        date = poll["end_datetime"]
        status = poll["voting_status"]
        options = poll["options"]
        # test print("\n", res_tweet)
        user = "dummy_user"
        # user_id=res["users"][0].id

        total = 0
        for opt in options:
            total = total + opt["votes"]

        tweet_data = {
            # "text": text,
            "duration": duration,
            "date": str(date),
            "status": status,
            "poll options": options,
            "user": user,
            "total": total,
        }
        # Converte il dizionario in una stringa JSON
        tweet_data_json = json.dumps(tweet_data)
        # content_text = urllib.parse.quote_plus(tweet_data_json, safe="/")
        content_text = urlencode(tweet_data_json, safe="/")
        # insert poll vote
        tweetdata = persistence.insert_answer_post(
            idpost=post,
            content=content_text,
            author=user,
            id_on_network=str(tweetid),
            publication_date=None,
            reply_to=None,
        )
        #
        self.get_all_answer_post(idpost=post, delall=False)
        # get all answer
        replies = persistence.get_answer_post(idpost=post)
        replies_all = []
        for r in replies:
            decoded_str = urldecode(r.content)
            content = json.loads(decoded_str)
            tdata = {
                "posts": [
                    {
                        "post_id": str(post),
                        "network": "mastodon",
                        "responses": [
                            {
                                "response_id": r.id,
                                "content": content,
                                "children": r.reply_to,
                                "user_response_name": r.author,
                            }
                        ],
                    }
                ]
            }
            replies_all.append(tdata)
        return replies_all

    def get_post_by_netid(self, tweetid: str, user: str):
        """https://mastodonpy.readthedocs.io/en/stable/02_return_values.html#status-dict"""
        data = {
            "id": 0,
            "created_at": datetime.now(),
            "content": "dummy_text",
        }

        content = {"type": "post", "content": {"text": data["content"]}}
        return persistence.reflect_post_social_user(
            tweetid, json.dumps(content), [], data["created_at"], user
        )

    def get_status(self):
        """application/rate_limit_status"""
        return {}
