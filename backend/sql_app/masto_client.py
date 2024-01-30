"""
# Sample API calls

https://fediscience.org/api/v1/instance
https://docs.joinmastodon.org/client/public/
https://qoto.org/api/v1/accounts/816974
https://qoto.org/api/v1/statuses/111718827325562462
https://qoto.org/api/v1/statuses/111543950452551643/context
https://fediscience.org/api/v1/statuses/111721301842093581
https://fediscience.org/api/v1/polls/155749
"""

from typing import Dict

import json
from datetime import datetime
from mastodon import MastodonError  # type: ignore

from settings import DEBUG

from .abstract_client import AbstractClient
from .database import SessionLocal
from . import persistence, models, media
from .masto_conn import MastodonEndpoint


class MastoClient(AbstractClient):
    sn_name = "MASTODON"
    sn_id = 2

    def __init__(self, settings_map: Dict[str, str]):
        self.setting = MastodonEndpoint(settings_map)
        self.client = self.setting.get_client()

    def insert_tweets(self, status: int, conten_str: str, idpost: int):
        visibility = "direct" if DEBUG else "public"
        list_res = []
        # devo cercare le immagini se ci sono e se sono legate al post
        dbimage = persistence.get_images_for_post(idpost)
        if dbimage:
            media = []
            for i in dbimage:
                try:
                    res = self.client.media_post(i[0])
                except MastodonError as e:
                    return {"error": str(e), "context": "Media upload"}
                media.append(res)
                print(i[0])
            try:
                new_tweet = self.client.status_post(
                    conten_str, media_ids=media, visibility=visibility
                )
            except MastodonError as e:
                return {
                    "error": str(e),
                    "context": "Post update status (create post)",
                }
        else:
            print("non ho trovato immagini")
            try:
                # new_tweet = self.api.update_status(conten_str)
                new_tweet = self.client.status_post(conten_str, visibility=visibility)
            except MastodonError as e:
                return {
                    "error": str(e),
                    "context": "Post update status (create post)",
                }

        # print(new_tweet)
        recordObject = {
            "status": "success" if new_tweet["id"] else "failure",
            "post": [
                {
                    "post_id": idpost,
                    "post_on_network_id": new_tweet["id"],
                    "network": "mastodon",
                }
            ],
        }
        if new_tweet.errors:
            recordObject["errors"] = new_tweet.errors

        list_res.append(recordObject)
        # print(list_res)
        # se ho id vuol dire che il messaggio è stato inviato
        # allora faccio aggiornamento dello stato e id_on_network del post
        # id_on_network da salvare sul db
        persistence.update_post_status_id_on_network(
            idpost=idpost,
            status=status + 1,
            id_on_net=new_tweet["id"],
            snet_id=self.sn_id,
        )

        return list_res

    def insert_poll(
        self, idpost: int, status: int, list_opt, text_poll: str, duration_minutes: int
    ):
        """creazione nuovo post di tipo poll su tw e sul db"""
        visibility = "direct" if DEBUG else "public"
        # ricordare: You can only provide one of poll or media
        newpoll = []
        try:
            newpoll = self.client.make_poll(
                options=list_opt,
                # text=text_poll,
                expires_in=duration_minutes,
                # user_auth=True,
            )
        except MastodonError as e:
            return {"error": str(e)}
        try:
            new_tweet = self.client.status_post(
                text_poll, visibility=visibility, poll=newpoll
            )
        except MastodonError as e:
            return {"error": str(e)}

        list_res = []
        if not new_tweet:
            recordObject = {
                "status": "failure",
                "post": [
                    {"post_id": idpost, "post_on_network_id": 0, "network": "mastodon"}
                ],
            }
        else:
            # recupero i dati che devo inserire nel db
            id_on_tweet = new_tweet["id"]

            persistence.update_post_status_id_on_network(
                idpost=idpost,
                status=status + 1,
                id_on_net=id_on_tweet,
                snet_id=self.sn_id,
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
        id = id_on_net
        try:
            status = self.api.status_reblogged_by(id)
        except MastodonError as e:
            return {"error": str(e)}
        source = status.source
        print("The source of the status is : " + source)
        retweet_count = status.retweet_count
        print(
            "The number of time the status has been retweeted is : "
            + str(retweet_count)
        )

    def get_all_answer_post(self, post_id: int, delall: bool = True):
        # 1)cancello tutte le risposte salvate e le riscarico da zero
        # 1) del answer post x
        if delall:
            persistence.delete_answer(post_id)

        # 2)scarico tutte le risposte e le salvo nel db
        tweetid = (
            SessionLocal()
            .query(models.Post.id_on_network)
            .filter_by(id=post_id)
            .scalar()
        )
        # print(tweetid)
        try:
            self.client.status(tweetid)
        except MastodonError as e:
            return {"error": str(e)}
        # print(t)
        # print(t["account"]["acct"])
        replies = []
        # user_name = user #nome senza @
        try:
            stw = self.client.status_context(tweetid)["descendants"]
        except MastodonError as e:
            return {"error": str(e)}
        for tweet in stw:
            # if hasattr(tweet, "in_reply_to_status_id_str"):
            # if tweet.in_reply_to_status_id_str == str(tweetid):
            # salvo nel db le risposte al tweetp
            dta_created_at = tweet["created_at"]

            # tweet_data_json = json.dumps({"text": tweet["content"]})
            content_text = json.dumps({"content": tweet["content"]})
            # content_text = urllib.parse.quote_plus(tweet_data_json, safe="/")
            # content_text = urlencode(tweet_data_json, safe="/")
            # content_text=urllib.parse.quote_plus(tweet.full_text)
            tweet_data = persistence.insert_answer_post(
                idpost=post_id,
                content=content_text,
                author=tweet["account"]["acct"],
                id_on_network=tweet["id"],
                publication_date=dta_created_at,
                reply_to=None,
                snet_id=self.sn_id,
            )
            # devo verificare se ci sono risposte a risposte
            self.get_all_answer_post_in_reply_to(
                postid=post_id, tweetid=tweet["id"], user=tweet["account"]["acct"]
            )

        # 3)faccio un get dal db delle risposta al posto
        # dopo aver inserito tutte le risposte nel db devo restituirele interrogando direttamente il db
        # self.get_all_retweet_post(tweetid, post=post_id)
        replies = persistence.get_answers_for_post(idpost=post_id)
        replies_all = []
        for r in replies:
            tdata = {
                "posts": [
                    {
                        "post_id": str(post_id),
                        "network": "mastodon",
                        "responses": [
                            {
                                "response_id": r.id,
                                # "content": urldecode(r.content),
                                "content": r.content,
                                "children": r.reply_to,
                                "user_response_name": r.author,
                            }
                        ],
                    }
                ]
            }
            replies_all.append(tdata)
        return replies_all

    def get_all_answer_post_in_reply_to(self, postid: int, tweetid: str, user: str):
        """get reply to answer (risposta a risposta)"""
        user_name = user  # nome senza @
        try:
            stw = self.client.status_context(tweetid)["descendants"]
        except MastodonError as e:
            return {"error": str(e)}

        for tweet in stw:
            # if hasattr(tweet, "in_reply_to_status_id_str"):
            #     if tweet.in_reply_to_status_id_str == str(tweetid):
            print("risposta:")
            # pp.pprint(tweet.__dict__)
            print(tweet["account"]["acct"])
            dta_created_at = tweet["created_at"]
            content_text = json.dumps({"content": tweet["content"]})
            # tweet_data_json = json.dumps({"text": tweet["content"]})
            # content_text = urllib.parse.quote_plus(tweet_data_json, safe="/")
            # content_text = urlencode(tweet_data_json, safe="/")
            # content_text=urllib.parse.quote_plus(tweet.full_text)
            tweet_data = persistence.insert_answer_post(
                idpost=postid,
                content=content_text,
                author=tweet["account"]["acct"],
                id_on_network=tweet["id"],
                publication_date=dta_created_at,
                reply_to=tweetid,
                snet_id=self.sn_id,
            )

        return None

    def get_poll_from_id(self, post_id: int):
        """get poll by id tweet. Also gets answers"""
        persistence.delete_answer(idpost=post_id)
        tweetid = (
            SessionLocal()
            .query(models.Post.id_on_network)
            .filter_by(id=post_id)
            .scalar()
        )
        try:
            tweet = self.client.status(tweetid)
        except MastodonError as e:
            return {"error": str(e)}

        poll = tweet["poll"]  # print (res)
        if not poll:
            raise TypeError("Provided tweet does not contain a poll!")

        duration = (poll["expires_at"] - tweet["created_at"]).total_seconds() / 60
        date = poll["expires_at"]
        status = "expired" if poll["expired"] else "open"
        options = poll["options"]
        text = {o["title"]: o["votes_count"] for o in poll["options"]}
        print(text)

        total = sum([opt["votes_count"] for opt in options])

        tweet_data = {
            "content": text,
            "duration_minute": int(duration),
            "date": date.isoformat(),
            "status": status,
            "poll_options": options,
            "total": total,
        }
        # Converte il dizionario in una stringa JSON
        # tweet_data_json = json.dumps(tweet_data)
        content_text = json.dumps(tweet_data)
        # content_text = urllib.parse.quote_plus(tweet_data_json, safe="/")
        # content_text = urlencode(tweet_data_json, safe="/")
        # insert poll vote
        tweetdata = persistence.insert_answer_post(
            idpost=post_id,
            content=content_text,
            id_on_network=str(tweetid),
            publication_date=datetime.now(),
            reply_to=str(tweetid),
            snet_id=self.sn_id,
        )
        #
        self.get_all_answer_post(post_id=post_id, delall=False)

        # get all answer
        replies = persistence.get_answers_for_post(idpost=post_id)
        replies_all = []
        for r in replies:
            print(r)
            print(r.content)
            # decoded_str = urldecode(r.content)
            decoded_str = r.content
            print(decoded_str)
            content = json.loads(decoded_str)
            tdata = {
                "posts": [
                    {
                        "post_id": str(post_id),
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

    """ 
    children---da chiedere
    Response body: {"posts": [{"post_id": "<post_id>", "network": "<facebook|mastodon>",
    "responses": [{"response_id": "<response_id>", "content": "<text>", "children": ["<response_id>"]}]}"}
    Get the responses to the posts matching the filter from the request URI """

    def get_post_by_netid(self, tweetid: str, user: str):
        """https://mastodonpy.readthedocs.io/en/stable/02_return_values.html#status-dict"""
        data = self.client.status(tweetid)
        print(tweetid, type(tweetid))
        print(data["id"], type(data["id"]))
        assert tweetid == str(data["id"])

        ctype = "poll" if "poll" in data and data["poll"] else "post"
        content = {"type": ctype, "content": {"content": data["content"]}}

        image_files = []
        if ctype == "poll":
            content["content"]["poll_options"] = data["poll"]["options"]  # type: ignore
        elif "media_attachments" in data:
            for m in data["media_attachments"]:
                if m["url"]:
                    u = m["url"]
                elif m["remote_url"]:
                    u = m["remote_url"]
                else:
                    u = m["preview_url"]
                fname = f'{m["id"]}-{u.split("/")[-1]}'
                image_files += [media.download(u, fname)]

        return persistence.reflect_post_social_user(
            tweetid, json.dumps(content), image_files, data["created_at"].date(), user
        )

    def get_status(self):
        """application/rate_limit_status"""
        return "No known limit imposition on Mastodon"
