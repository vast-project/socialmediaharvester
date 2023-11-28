MEDIA_DIR = "/data"

TWITTER = 1
# This dictionary contains expected length of keys for validation
TWITTER_KEYS = {
    "access_token": 50,
    "access_token_secret": 45,
    "api_key": 25,
    "api_key_secret": 50,
    "bearer_token": 116,
    "client_ID": 34,
    "client_Secret": 50,
}

TWITTER_MAX_LEN = 280

TWITTER_MAX_POLL_DURATION = 7 * 24 * 60

# da salvare i dati del db in un file di configurazione
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:xxxxx@localhost:5532/islab_tweet"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:xxxxx@172.20.27.81:5532/islab_tweet"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:xxxxx@tacitserver:5532/islab_tweet"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:xxxxx@islab_tweet_db/islab_tweet"

VERSION = "0.1.2"
