"""Web service endpoints responsible for post (and poll) management"""
from typing import List, Optional

from datetime import date, datetime
import json

# from typing import Annotated
from fastapi import Depends, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

import logging

logger = logging.getLogger()

from util import urlencode, urldecode
from sql_app import persistence, schemas, social

# from sql_app.database import SessionLocal

# pp = pprint.PrettyPrinter(indent=4)

router = APIRouter()
security = HTTPBasic()

from settings import TWITTER_MAX_LEN, TWITTER_MAX_POLL_DURATION


# @router.get("/network/{network}/schedule/")
@router.get("/")
# @router.get("/schedule/")
async def get_posts(
    credentials: HTTPBasicCredentials = Depends(security), network_id: int = 1
):
    """Get all posts managed by our users. This is different from getting the respective responses."""
    values = persistence.get_post_by_status(credentials.username)  # status=status)
    list = []
    for v in values:
        data = json.loads(v.content)
        recordObject = {
            "post_id": v.id,
            "author": v.author,
            "network": persistence.get_network_name(network_id)["s_name"],
            "status": persistence.get_status_by_id(idstatus=v.status)["status_name"],
            "text": urldecode(data["content"]["text"]),
            "answers": 0,  # TODO
            "due": v.scheduling_date,
            "id_on_network": v.id_on_network,
            "type": data["type"],
        }
        list.append(recordObject)
    return {"status": list}


@router.get("/aut_appstatus/")
async def get_status(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Documentazione - rate_limit_status
    -------------------
    **Response:**
    - 200 OK: status limit/remaining
    - 404 Not Found
    """
    values = social.get_aut_status(credentials.username)
    return values


###################
# @router.post("/network/{social_network}/content/{content}")
# @router.post("/network/{social_network}/content/{content}/due/{date_sched}")
@router.post("/content/{content}/due/{date_sched}")
@router.post("/content/{content}")
async def post_content(
    content: str,
    date_sched: Optional[date] = None,
    files: Optional[List[schemas.ImageBase]] = None,
    credentials: HTTPBasicCredentials = Depends(security),
    social_network_id: int = 1,
):
    """
    - content: test of post, use %0a for new line
    - Optional list image  - absolute path of the images
    - Date format ISO: YYYY-MM-DD
    """
    content_text = urlencode(content)
    if len(content_text) > TWITTER_MAX_LEN:
        raise ValueError(
            f"Content too long. A maximum of {TWITTER_MAX_LEN} characters is allowed."
        )

    print(content_text)
    content_dict = {"type": "post", "content": {"text": content_text}}
    print(json.dumps(content_dict))
    # Salvare le immagini nella tabella delle immagini
    imgs = [v.path for v in files] if files else []
    if len(imgs) > 4:
        raise HTTPException(405, "Only up to 4 images are allowed")
    # Verifica che date_sched sia una data
    if not date_sched:
        date_sched = datetime.today()
    elif not isinstance(date_sched, date):
        raise ValueError("Il parametro date_sched deve rappresentare solo una data")
    print(content_dict)

    result = persistence.create_post_social_user(
        post_content=json.dumps(content_dict),
        pathimages=imgs,
        sched_date=date_sched,
        user=credentials.username,
    )
    return JSONResponse(content=jsonable_encoder(result))


# @router.post("/poll/network/{social_network_id}/content/{content}/due/{date_sched}")
@router.post("/poll/content/{content}")
@router.post("/poll/content/{content}/due/{date_sched}")
async def post_poll_content(
    content: str,
    opt1: str,
    opt2: str,
    opt3: Optional[str] = None,
    opt4: Optional[str] = None,
    date_sched: Optional[date] = None,
    duration_minute: int = TWITTER_MAX_POLL_DURATION,
    social_network_id: int = 1,
    credentials: HTTPBasicCredentials = Depends(security),
):
    poll_options = [urldecode(o) for o in [opt1, opt2, opt3, opt4] if o]

    # content_text = urllib.parse.quote_plus(content)
    content_text = urlencode(content)
    content_dict = {
        "type": "poll",
        "content": {
            "text": content_text,
            "poll_options": poll_options,
            "duration_minute": duration_minute,
        },
    }

    # Verifica che date_sched sia una data
    if not date_sched:
        date_sched = datetime.today()
    if not isinstance(date_sched, date):
        raise ValueError("Il parametro date_sched deve rappresentare solo una data")

    # Verifica che duration_minute sia un intero positivo
    if not isinstance(duration_minute, int) or duration_minute <= 4:
        raise ValueError(
            "Il parametro duration_minute deve essere un intero positivo e deve avere un valore >=5"
        )

    result = persistence.create_post_social_user(
        post_content=json.dumps(content_dict),
        user=credentials.username,
        pathimages=[],
        sched_date=date_sched,
    )
    return result


# put
@router.patch("/{idpost}")
async def update_post(
    idpost: int,
    status: int,
    sched_date: Optional[date] = None,
    content: Optional[str] = None,
):
    if not isinstance(idpost, int) or idpost <= 0:
        raise ValueError("L'idpost deve essere un intero positivo")
    if status not in (1, 2):
        raise ValueError(
            "Lo stato del post deve essere 1 (Created), 1 (Scheduled for publication)"
        )
    if content is not None and len(content) > 280:
        raise ValueError("Il contenuto del post non può superare i 280 caratteri")
    if sched_date is not None and sched_date <= date.today():
        raise ValueError(
            "La data di programmazione del post deve essere maggiore della data corrente"
        )

    if content:
        content_text = urlencode(content)
        content_dict = {"type": "post", "content": {"text": content_text}}
    else:
        content_dict = {}

    updated = persistence.update_post(
        idpost=idpost,
        post_content=str(content_dict),
        status_post=status,
        sched_date=sched_date,
    )
    if updated:
        return {"message": "Post aggiornato correttamente"}
    else:
        raise ValueError("Impossibile aggiornare il post con l'id specificato")


# delete
@router.delete("/{idpost}")
async def delete_post(idpost: int):
    return persistence.delete_post(idpost=idpost)


# # GET /post/network/<network>/status/<status>/schedule
# # @router.get("/network/{network_id}/status/{status}/schedule/")
# @router.get("/status/{status}/schedule/")
# async def get_schedule_post(status: int, network_id: int = 1):
#     values = persistence.get_post_status(status=status)
#     list = []
#     for v in values:
#         recordObject = {
#             "post_id": v.id,
#             "network": persistence.get_network_name(network_id),
#             "status": persistence.get_status_by_id(idstatus=v.status),
#             "due": v.scheduling_date,
#         }
#         list.append(recordObject)
#     return {"status": list}


# @router.get("/network/{network_id}/flush")
@router.get("/flush")
async def flush_post(
    network_id: int = 1, credentials: HTTPBasicCredentials = Depends(security)
):
    """
    When network is ommitted, it defaults to Twitter.
    """
    db_post = persistence.get_post_by_status(credentials.username, status=2)
    if not db_post:
        return {"message": f"Nessun post con status 2!!"}
    return {
        "message": social.insert_all_pending_tweets(
            snet_id=network_id, status=2, user=credentials.username
        )
    }


# scarica tutte le risposte a un determinato tweet
# @router.get("/network/{network}/post/{post_id}/responses/")
@router.get("/post/{post_id}/responses/")
async def read_answer_tweet(
    post_id: int,
    network_id: int = 1,
    credentials: HTTPBasicCredentials = Depends(security),
):
    """GET /post/responses
    GET /post/network/<network>/responses
    GET /post/network/<network>/post/<post_id>/responses
    Request body: none
    Response body: {"posts": [{"post_id": "<post_id>", "network": "<facebook|twitter>", "responses": [{"response_id": "<response_id>", "content": "<text>", "children": ["<response_id>"]}]}"}
    Get the responses to the posts matching the filter from the request URI"""
    if not post_id:
        return {"message": "no tweet ID parameter"}
    return {
        "message": social.get_all_answer_post(
            snet_id=network_id, tweetid=post_id, user=credentials.username
        )
    }


# @router.get("/network/{network}/poll/{post_id}/responses/")
@router.get("/poll/{post_id}/responses/")
async def read_answer_poll(
    post_id: int,
    network_id: int = 1,
    credentials: HTTPBasicCredentials = Depends(security),
):
    """When network is ommitted, it defaults to Twitter."""
    return {
        "message": social.get_poll_from_id(
            snet_id=network_id, tweetid=post_id, user=credentials.username
        )
    }


# @router.get("/network/{network}/{post_id}/responses_inDB/")
@router.get("/{post_id}/responses_inDB/")
async def read_answer_post(post_id: int):
    """When network is ommitted, it defaults to Twitter."""
    values = persistence.get_answer_post(idpost=post_id)
    list = []
    for v in values:
        recordObject = {
            "post_id": v.id,
            "author": v.author,
            "publication_date": v.publication_date,
            "text": urldecode(v.content),
            "id_on_network": v.id_on_network,
            "reply_to": v.reply_to,
        }
        list.append(recordObject)
    post_item = persistence.get_post_by_id(post_id)  # status=status)
    if not post_item:
        raise HTTPException(404, detail="Post not found")
    data = post_item.content
    post = {
        "type": data["type"],
        "author": post_item.author,
        "text": data["content"]["text"],
        "id_on_network": post_item.id_on_network,
    }
    # TODO: Images
    # images = ["/data/islab.jpg"]
    images = persistence.get_images_for_post(post_id)
    if images:
        post["images"] = images

    # TODO: Poll results
    poll_results = {"yes": 10, "no": 5}
    # poll_results = persistence.get_answer_post()
    if poll_results:
        post["poll_options"] = poll_results

    return {"post": post, "answers": list}

    # return {"message": persistence.get_answer_post(idpost=post_id)}


# TODO->get quote tweet

""" @router.get("/network/{network}/post/{post_id}/quote/")
async def read_answer_quote(network: int, post_id:int):
    social.get_all_quote_post( post=post_id)

    return None
 """
