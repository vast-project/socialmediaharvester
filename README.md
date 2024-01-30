# SocialMediaHarvester

## Features

This service is meant to allow for:

1. Scheduling of posts on social media (currently Fediverse/Mastodon and Twitter), including containing images and polls
2. Collecting (we refer to this as harvesting) responses both as replies and poll votes. Currently, collection of reblogs/boosts with comments is not supported.

## Deployment
OpenAPI interface is accessible from ISLab VPN at http://172.20.27.81:8090
The DB is accessibile at postgres@172.20.27.81:5532/islab_tweet

User handling is performed with a mock using HTTP Basic Auth. Password is not verified, user must coincide with the one of the user of the social network.

To add a new user, its keys need to be added to the DB table socialcampaigns.setting, as [shown here](https://github.com/umilISLab/IslabTweet/blob/main/ScriptDB/z_init.sql)

To deploy frontend, run:

    npm install && npm run build

To deploy backend, run:

    docker exec -it socialmediaharvester_app python init.py

# Dependency Tree

```mermaid
graph LR
    main --> post & identity & fetch
    identity --> persistence
    fetch --> social
    post --> persistence & schemas & social 
    persistence --> database & models & schemas & query
    query --> models
    social --> abstract_client
    twitter_client & masto_client & dummy_client --> abstract_client
    abstract_client --> persistence & models
    models --> database
    twitter_client --> twitter_conn, media
    masto_client --> masto_conn, media
    twitter_conn & masto_conn --> models
```