"""OBSOLETE: Twitter/X API has been disabled"""

from typing import Dict, List

import json

from .abstract_client import AbstractClient
import tweepy  # type: ignore
from tweepy.errors import TweepyException  # type: ignore

from util import urlencode, urldecode

from .database import SessionLocal
from . import twitter_conn, persistence, models, media

# pp = pprint.PrettyPrinter(indent=4)  # uso per debug


class TwitterClient(AbstractClient):
    sn_name = "TWITTTER"
    sn_id = 1

    def __init__(self, settings_map: Dict[str, str]):
        self.setting = twitter_conn.TwitterEndpoint(settings_map)
        self.api = self.setting.get_setting()  # Twitter API v1.1
        self.client = self.setting.get_client()  # Twitter API v2.0

    def insert_tweets(self, status: int, conten_str: str, idpost=int):
        # parametri satus=2 -->Scheduled for publication
        # dbpost = (
        #     db.query(models.Post.content, models.Post.id)
        #     .filter(models.Post.status == status)
        #     .all()
        # )
        list_res = []
        # devo cercare le immagini se ci sono e se sono legate al post
        dbimage = persistence.get_images_for_post(idpost)
        media = []
        if dbimage:
            for i in dbimage:
                try:
                    res = self.api.media_upload(i[0])
                except TweepyException as e:
                    return {"error": str(e), "context": "API v1.1 Media upload"}
                media.append(res.media_id)
                print(i[0])
            try:
                new_tweet = self.client.create_tweet(text=conten_str, media_ids=media)
            except TweepyException as e:
                return {
                    "error": str(e),
                    "context": "API v2.0 Tweet update status (create tweet)",
                }
        else:
            print("non ho trovato immagini")
            try:
                # new_tweet = self.api.update_status(conten_str)
                new_tweet = self.client.create_tweet(text=conten_str)
            except TweepyException as e:
                return {
                    "error": str(e),
                    "context": "API v2.0 Tweet update status (create tweet)",
                }

        # print(new_tweet)
        recordObject = {
            "status": "success" if new_tweet.data["id"] else "failure",
            "post": [{"post_id": idpost, "post_on_network_id": 0, "network": "twitter"}]
            # "messaggio":new_message,
            # "id_on_tweet": 0
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
            id_on_net=new_tweet.data["id"],
            s_network=self.sn_id,
        )

        return list_res

    # creazione nuovo post di tipo poll su tw e sul db
    def insert_poll(
        self, idpost: int, status: int, list_opt, text_poll: str, duration_minutes: int
    ):
        # ricordare: You can only provide one of poll or media
        newpoll = []
        try:
            newpoll = self.client.create_tweet(
                text=text_poll,
                poll_options=list_opt,
                poll_duration_minutes=duration_minutes,
                user_auth=True,
            )
        except TweepyException as e:
            return {"error": str(e)}

        list_res = []
        if not newpoll:
            recordObject = {
                "status": "failure",
                "post": [
                    {"post_id": idpost, "post_on_network_id": 0, "network": "twitter"}
                ],
            }
        else:
            # recupero i dati che devo inserire nel db
            poll = newpoll[0]  # print (res)
            id_on_tweet = poll["id"]

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
                        "network": "twitter",
                    }
                ],
            }
        list_res.append(recordObject)
        return list_res

    def print_first_public_tweet(self):
        try:
            public_tweets = self.api.home_timeline()
        except TweepyException as e:
            return {"error": str(e)}

        return {
            "created_at": public_tweets[0].created_at,
            "text": public_tweets[0].text,
            "name": public_tweets[0].user.screen_name,
        }

    # def print_search_tweets(self, q_str: str):
    #     try:
    #         stw = self.api.search_tweets
    #     except TweepyException as e:
    #         return {"error": str(e)}

    #     public_tweets = tweepy.Cursor(
    #         stw, q=q_str, result_type="mixed", tweet_mode="extended"
    #     ).items(10)

    #     result = []
    #     for tweet in public_tweets:
    #         print("@" + tweet.user.screen_name)
    #         tweet_text = tweet.full_text
    #         print(tweet_text)
    #         print(f"\nRicerca per -->  {q_str}\n")
    #         result += [{"text": tweet_text, "user": "@" + tweet.user.screen_name}]
    #     return result

    # def print_search_byuser(self, usr: str, max_tweet: int):
    #     # ricerca per utente
    #     user = usr
    #     limit = max_tweet
    #     try:
    #         tweets = self.api.user_timeline(
    #             screen_name=user, count=limit, tweet_mode="extended"
    #         )
    #     except TweepyException as e:
    #         return {"error": str(e)}

    #     result = []
    #     for tweet in tweets:
    #         r = {
    #             "user": "@" + tweet.user.screen_name,
    #             "text": tweet.full_text,
    #             "*": "*******************",
    #         }
    #         result.append(r)
    #     return result

    def status_retweeted(self, id_on_net):
        # the ID of the status
        id = id_on_net
        try:
            status = self.api.get_status(id)
        except TweepyException as e:
            return {"error": str(e)}
        source = status.source
        print("The source of the status is : " + source)
        retweet_count = status.retweet_count
        print(
            "The number of time the status has been retweeted is : "
            + str(retweet_count)
        )

    # def put_userid(self, usr: str):
    #     # using user.id
    #     put_your_screen_name = usr
    #     try:
    #         user = self.api.get_user(screen_name=put_your_screen_name)
    #     except TweepyException as e:
    #         return {"error": str(e)}

    #     result = [{"ID": user.id, "user": "@" + user.name}]
    #     return result

    # def get_poll_from_user(self, username: str):
    #     # esempio trovato in tweepypoll e su https://developer.twitter.com
    #     # prende tutti i poll che trova di un determinato utente
    #     users = []
    #     try:
    #         users = self.client.get_users(
    #             usernames=username, user_fields=["id"]
    #         )  # test print (users, "" , username)
    #     except TweepyException as e:
    #         return {"error": str(e)}
    #     # costruisco lista di id di sondaggi/pool

    #     if users is not None and any(users):
    #         print(any(users))
    #         for user in users.data:  # type: ignore
    #             user_id = user.id
    #             # print (user_id, "\n")
    #     # Get tweets -- funzione get_tweets su client.py
    #     try:
    #         tweets = self.client.get_users_tweets(
    #             id=user_id,
    #             max_results=100,
    #             exclude=["retweets", "replies"],
    #             expansions="attachments.poll_ids",
    #         )
    #     except TweepyException as e:
    #         return {"error": str(e)}

    #     # Get -- tweet_id che contengono sondaggi
    #     tweet_id_with_poll = []
    #     for tweet in tweets.data:
    #         if "attachments" in tweet.data.keys():
    #             # print("Id_su:") - print(tweet.id)
    #             tweet_id_with_poll.append(tweet.id)
    #         else:
    #             pass
    #     rtn = []
    #     for tweet_id in tweet_id_with_poll:
    #         print("Id_giu:")
    #         print(tweet_id)
    #         try:
    #             res_tweet = self.client.get_tweets(
    #                 tweet_id,
    #                 expansions=["attachments.poll_ids", "author_id"],
    #                 poll_fields=["duration_minutes", "end_datetime", "voting_status"],
    #                 # dal sito https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent
    #                 # enum (duration_minutes, end_datetime, id, options, voting_status)
    #                 # curl --request GET 'https://api.twitter.com/2/tweets?ids=1199786642791452673&expansions=attachments.poll_ids&poll.fields=duration_minutes,end_datetime,id,options,voting_status' --header 'Authorization: Bearer $BEARER_TOKEN'
    #             )
    #         except TweepyException as e:
    #             return {"error": str(e)}
    #         res = res_tweet.includes  # recupero i risultati

    #         try:
    #             res["polls"][0]
    #         except KeyError:
    #             raise TypeError("Provided tweet does not contain a poll!")

    #         poll = res["polls"][0]  # print (res)
    #         duration = poll["duration_minutes"]
    #         date = poll["end_datetime"]
    #         status = poll["voting_status"]
    #         options = poll["options"]
    #         text = res_tweet.data[0]["text"]
    #         # test print("\n", res_tweet)
    #         user = res["users"][0].username

    #         total = 0
    #         for opt in options:
    #             total = total + opt["votes"]

    #         tweet_data = {
    #             "text": text,
    #             "duration": duration,
    #             "date": date,
    #             "status": status,
    #             "poll options": options,
    #             "user": user,
    #             "total": total,
    #         }
    #         rtn.append(tweet_data)
    #     return rtn

    # def get_all_answer(self, username, tweetid):
    #     """ risposte ad un tweet """
    #     replies = []
    #     try:
    #         stw = self.api.search_tweets
    #     except TweepyException as e:
    #         return {"error": str(e)}
    #     for tweet_all in tweepy.Cursor(
    #         stw,
    #         q="to:" + username,
    #         result_type="recent",
    #         tweet_mode="extended",
    #     ).items(1000):
    #         if hasattr(tweet_all, "in_reply_to_status_id_str"):
    #             if tweet_all.in_reply_to_status_id_str == tweetid:
    #                 tweet_data = {
    #                     "id": tweet_all.id,
    #                     "full_text": tweet_all.full_text,
    #                     "created_at": tweet_all.created_at,
    #                     "user_response_id": tweet_all.user.id,
    #                     "user_response_name": tweet_all.user.name,
    #                 }
    #                 replies.append(tweet_data)
    #     return replies

    # # esempio trovato in https://www.thinkingondata.com/exploring-the-replies-from-a-question-in-twitter-using-python-and-r/
    # def get_quote_post(self, idpost: int):
    #     try:
    #         tweet = self.api.get_status(idpost, tweet_mode="extended")
    #     except TweepyException as e:
    #         return {"error": str(e)}
    #     # Numero di citazioni del tweet
    #     quote_count = tweet.quote_count
    #     return quote_count

    def get_all_answer_post(self, idpost: int, delall: bool = True):
        # 1)cancello tutte le risposte salvate e le riscarico da zero
        # 1) del answer post x
        if delall:
            del_answer = persistence.delete_answer(idpost=idpost)

        # 2)scarico tutte le risposte e le salvo nel db
        tweetid = (
            SessionLocal()
            .query(models.Post.id_on_network)
            .filter_by(id=idpost)
            .scalar()
        )
        print(tweetid)
        try:
            t = self.api.get_status(tweetid)
        except TweepyException as e:
            return {"error": str(e)}
        u = t.user
        user_name = u.screen_name
        print(user_name)
        replies = []
        # user_name = user #nome senza @
        try:
            stw = self.api.search_tweets
        except TweepyException as e:
            return {"error": str(e)}
        for tweet in tweepy.Cursor(
            stw,
            q="to:" + user_name,
            since_id=tweetid,
            tweet_mode="extended",
        ).items():
            if hasattr(tweet, "in_reply_to_status_id_str"):
                if tweet.in_reply_to_status_id_str == str(tweetid):
                    # salvo nel db le risposte al tweetp
                    data_ora = tweet.created_at
                    dta_created_at = data_ora

                    tweet_data_json = json.dumps(tweet.full_text)
                    content_text = urlencode(tweet_data_json)
                    # content_text=urllib.parse.quote_plus(tweet.full_text)
                    tweet_data = persistence.insert_answer_post(
                        idpost=idpost,
                        content=content_text,
                        author=tweet.user.screen_name,
                        id_on_network=str(tweet.id),
                        publication_date=dta_created_at,
                        reply_to=None,
                    )
                    # devo verificare se ci sono risposte a risposte
                    self.get_all_answer_post_in_reply_to(
                        postid=idpost, tweetid=tweet.id, user=tweet.user.screen_name
                    )

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
                        "network": "twitter",
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
        # name = 'B_MCristina'
        user_name = user  # nome senza @
        try:
            stw = self.api.search_tweets
        except TweepyException as e:
            return {"error": str(e)}

        for tweet in tweepy.Cursor(
            stw,
            q="to:" + user_name,
            since_id=tweetid,
            tweet_mode="extended",
        ).items():
            if hasattr(tweet, "in_reply_to_status_id_str"):
                if tweet.in_reply_to_status_id_str == str(tweetid):
                    print("risposta:")
                    # pp.pprint(tweet.__dict__)
                    print(tweet.user.screen_name)
                    data_ora = tweet.created_at
                    dta_created_at = data_ora.strftime("%Y-%m-%d")
                    tweet_data_json = json.dumps(tweet.full_text)
                    content_text = urlencode(tweet_data_json)
                    # content_text=urllib.parse.quote_plus(tweet.full_text)
                    tweet_data = persistence.insert_answer_post(
                        idpost=postid,
                        content=content_text,
                        author=tweet.user.screen_name,
                        id_on_network=str(tweet.id),
                        publication_date=dta_created_at,
                        reply_to=tweetid,
                    )

        return None

    # get poll by id tweet
    def get_poll_from_id(self, post_id: int):
        del_answer = persistence.delete_answer(idpost=post_id)
        tweetid = (
            SessionLocal().query(models.Post.id_on_network).filter_by(id=post_id).scalar()
        )
        try:
            res_tweet = self.client.get_tweets(
                tweetid,
                expansions=["attachments.poll_ids", "author_id"],
                poll_fields=["duration_minutes", "end_datetime", "voting_status"],
            )
        except TweepyException as e:
            return {"error": str(e)}
        res = res_tweet.includes  # recupero i risultati

        try:
            res["polls"][0]
        except KeyError:
            raise TypeError("Provided tweet does not contain a poll!")

        poll = res["polls"][0]  # print (res)
        duration = poll["duration_minutes"]
        date = poll["end_datetime"]
        status = poll["voting_status"]
        options = poll["options"]
        print(res_tweet.data[0])
        # test print("\n", res_tweet)
        user = res["users"][0].username
        # user_id=res["users"][0].id

        total = 0
        for opt in options:
            total = total + opt["votes"]

        tweet_data = {
            # "text": res_tweet.data[0]["text"],
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
            idpost=post_id,
            content=content_text,
            author=user,
            id_on_network=str(tweetid),
            publication_date=None,
            reply_to=None,
        )
        #
        self.get_all_answer_post(idpost=post_id, delall=False)
        # get all answer
        replies = persistence.get_answer_post(idpost=post_id)
        replies_all = []
        for r in replies:
            decoded_str = urldecode(r.content)
            content = json.loads(decoded_str)
            tdata = {
                "posts": [
                    {
                        "post_id": str(post_id),
                        "network": "twitter",
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
    Response body: {"posts": [{"post_id": "<post_id>", "network": "<facebook|twitter>",
    "responses": [{"response_id": "<response_id>", "content": "<text>", "children": ["<response_id>"]}]}"}
    Get the responses to the posts matching the filter from the request URI """

    # def get_all_retweet_post(self, tweetid, post: int):
    #     try:
    #         retweets = self.api.get_retweets(tweetid)
    #     except TweepyException as e:
    #         return {"error": str(e)}
    #     for retweet in retweets:
    #         # if retweet.user.id==49288229:
    #         # pp.pprint(retweet.__dict__)
    #         print(
    #             f"{tweetid}, {retweet.id}, {retweet.user.id}, data:{retweet.created_at}"
    #         )
    #         data_ora = retweet.created_at
    #         dta_created_at = data_ora.strftime("%Y-%m-%d")
    #         try:
    #             t = self.api.get_status(retweet.id)
    #         except TweepyException as e:
    #             return {"error": str(e)}
    #         u = t.user
    #         user_name = u.screen_name
    #         tweet_data_json = json.dumps("#retweet#")
    #         content_text = urlencode(tweet_data_json)
    #         tweet_data = persistence.insert_answer_post(
    #             idpost=post,
    #             content=content_text,
    #             author=user_name,
    #             id_on_network=str(retweet.id),
    #             publication_date=dta_created_at,
    #             reply_to=None,
    #         )

    #     return None

    def get_post_by_netid(self, tweetid: str, user: str):
        expansions = [
            "attachments.poll_ids",
            "attachments.media_keys",
            "author_id",
            "edit_history_tweet_ids",
            "entities.mentions.username",
            "in_reply_to_user_id",
            "referenced_tweets.id",
            "referenced_tweets.id.author_id",
        ]
        media_fields = [
            "media_key",
            "type",
            "url",
            "public_metrics",
            "non_public_metrics",
            "organic_metrics",
            "promoted_metrics",
            "variants",
        ]
        poll_fields = [
            "duration_minutes",
            "end_datetime",
            "id",
            "options",
            "voting_status",
        ]
        tweet_fields = [
            "attachments",
            "author_id",
            "context_annotations",
            "conversation_id",
            "created_at",
            "edit_controls",
            "entities",
            "id",
            "possibly_sensitive",
            "referenced_tweets",
            "reply_settings",
            "source",
            "text",
            "withheld",
        ]
        data = self.client.get_tweet(
            tweetid,
            expansions=expansions,
            media_fields=media_fields,
            poll_fields=poll_fields,
            tweet_fields=tweet_fields,
        )

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
            options: List[str] = [
                o["label"] for o in data.includes["polls"][0]["options"]
            ]
            content["content"]["poll_options"] = options  # type: ignore
            content["type"] = "poll"
            # TODO: duration seems to be missing

        return persistence.reflect_post_social_user(
            tweetid, json.dumps(content), image_files, publ_date, user
        )

    def get_status(self):
        """application/rate_limit_status"""
        return self.api.rate_limit_status()


"""     #get quote(citazioni).... todo penso si a un problema di profilo 
    def get_all_quote_post(self, post_id):
        tweetid = SessionLocal().query(models.Post.id_on_network).filter_by(id=post_id).scalar()
        t = self.api.get_status(tweetid)
        u = t.user
        user_name = u.screen_name
        # definizione dei parametri di ricerca
        # Estrai i dettagli del tweet

        # ID del Tweet di cui cercare i Retweet con commento
        tweet_id = str(tweetid)  
        # Cerca tutti i retweet con commento del tweet specificato
        query =  'url:https://twitter.com/2/tweets/' +user_name +'/quote_tweets'.format(tweet_id)
        tweets = self.api.search_tweets(q=query)

        # Stampa i testi dei tweet trovati
        for tweet in tweets:
            print(tweet.text)

        return None """
