import os

VERSION = "0.2.0"

DEBUG = True

MEDIA_DIR = "/data"

# Social network also defined in ./db/init
SOCIAL_NETWORK_CLASS = "twitter_client.TwitterClient"
SOCIAL_NETWORK_CLASS = "masto_client.MastoClient"
# SOCIAL_NETWORK_CLASS = "dummy_client.DummyClient"

# da salvare i dati del db in un file di configurazione
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:xxxxx@localhost:5532/islab_tweet"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:xxxxx@172.20.27.81:5532/islab_tweet"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:xxxxx@tacitserver:5532/islab_tweet"
# User also defined in docker-compose.yml and ./db/init
SQLALCHEMY_DATABASE_URL = (
    "postgresql://postgres:xxxxxx@postgres/socialmediaharvester"
    # "postgresql://postgres:xxxxxx@localhost:5532/socialmediaharvester"
)

SERVER_SETTINGS = {
    # Twitter
    1: {
        "MAX_LEN": 280,
        # in minutes: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/poll
        "MAX_POLL_DURATION": 7 * 24 * 60,
    },
    # fediscience.org
    2: {
        "MAX_LEN": 500,
        # in seconds: https://mastodonpy.readthedocs.io/en/stable/05_statuses.html#make-poll
        "MAX_POLL_DURATION": 7 * 24 * 60 * 60,
    },
}

MASTO_APPNAME = "github.com/vast-project/socialmediaharvester"
MASTO_FILE = os.path.abspath("socialmediaharvester_mastodon.secret")
TOKEN_FILE = os.path.abspath("socialmediaharvester_mastodon.token")
