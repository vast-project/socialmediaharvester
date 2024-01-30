import json

from util import urldecode

from .database import SessionLocal
from . import models


class AbstractClient:
    """The current implementation supports a single social network,
    that is configured from settings. Thus this id is at the abstract level
    """

    sn_id = 0

    # def __init__(self, settings_map: Dict[str, str]):
    #     raise NotImplementedError("abstract method")

    def insert_all_pending_tweets(self, user: str, status: int = 2):
        db = SessionLocal()
        dbpost = (
            db.query(models.Post.content, models.Post.id)
            .filter(
                models.Post.status == status,
                models.Post.author == user,
                models.Post.s_network == self.sn_id,
            )
            .all()
        )
        media = []
        for post in dbpost:
            message = post[0]
            idpostindb = post[1]
            content = message
            content_diz = json.loads(content)
            # print(content_diz)

            if content_diz["type"] == "post":
                print(content_diz["content"]["text"])
                recordObject = self.insert_tweets(
                    status=2,
                    conten_str=urldecode(content_diz["content"]["text"]),
                    idpost=idpostindb,
                )
            else:
                print(content_diz["content"]["text"])
                recordObject = self.insert_poll(
                    idpost=idpostindb,
                    status=2,
                    list_opt=[
                        urldecode(o) for o in content_diz["content"]["poll_options"]
                    ],
                    text_poll=urldecode(content_diz["content"]["text"]),
                    duration_minutes=int(content_diz["content"]["duration_minute"]),
                )

            media.append(recordObject)
        return media

    def insert_tweets(self, status: int, conten_str: str, idpost: int):
        raise NotImplementedError("abstract method")

    def insert_poll(
        self, idpost: int, status: int, list_opt, text_poll: str, duration_minutes: int
    ):
        """creazione nuovo post di tipo poll su tw e sul db"""
        raise NotImplementedError("abstract method")

    def status_retweeted(self, id_on_net: str):
        raise NotImplementedError("abstract method")

    def get_all_answer_post(self, idpost: int, delall: bool = True):
        raise NotImplementedError("abstract method")

    def get_all_answer_post_in_reply_to(self, postid: int, tweetid: str, user: str):
        """get reply to answer (risposta a risposta)"""
        raise NotImplementedError("abstract method")

    def get_poll_from_id(self, post: int):
        """get poll by id tweet"""
        raise NotImplementedError("abstract method")

    # def get_all_retweet_post(self, tweetid: str, post: int):
    #     """
    #     children---da chiedere
    #     Response body: {"posts": [{"post_id": "<post_id>", "network": "<facebook|twitter>",
    #     "responses": [{"response_id": "<response_id>", "content": "<text>", "children": ["<response_id>"]}]}"}
    #     Get the responses to the posts matching the filter from the request URI"""
    #     raise NotImplementedError("abstract method")

    def get_post_by_netid(self, tweetid: str, user: str):
        raise NotImplementedError("abstract method")

    def get_status(self):
        """application/rate_limit_status"""
        raise NotImplementedError("abstract method")
