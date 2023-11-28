"""Calls to the DB layer from outside.
These manage persistence on their own.
Whenever queries are reused internally (from methods here),
these should go in query.py,
and session should be managed here."""

from typing import Dict, List, Optional

from datetime import date

from sqlalchemy.exc import IntegrityError  # type: ignore

from .query import create_image, get_post_by_snid
from .database import SessionLocal
from . import models, schemas


############################ user ######################################
# get user_by_user_name
def get_user_by_name(username: str) -> Optional[models.AppUser]:
    db = SessionLocal()
    print(username)
    user = db.query(models.AppUser).filter(models.AppUser.username == username).first()
    return user


# get user  0-limit mostra tutti gli utenti salvati nella tabella appuser
def get_users():
    db = SessionLocal()
    return db.query(models.AppUser).all()


def get_network_name(network_id: int):
    db = SessionLocal()
    return (
        db.query(models.Social_Network.s_name)
        .filter(models.Social_Network.id == network_id)
        .first()
    )


# post USER ---  add user
def create_user(user: schemas.UserCreate):
    db = SessionLocal()
    # npassword = user.password #passo il valore direttamente qua mettere md5 (da vedere)
    db_user = models.AppUser(**user.dict(), is_active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


##################################################################################
############################ social network ######################################
def get_snetwork_by_name(s_name: str):
    db = SessionLocal()
    return (
        db.query(models.Social_Network)
        .filter(models.Social_Network.s_name == s_name)
        .first()
    )


# get social  0-limit
def get_snetwork():
    db = SessionLocal()
    return db.query(models.Social_Network).all()


# # get name of snetwork
# def get_snetwork_by_id(s_net: str):
#     db = SessionLocal()
#     return (
#         db.query(models.Social_Network.s_name)
#         .filter(models.Social_Network.id == s_net)
#         .first()
#     )


# post Socialnetwork ---  tab Social_Network
def create_snetwork(sname: schemas.Social_NetworkCreate):
    db = SessionLocal()
    snamesocialnetwork = sname.s_name.upper()
    db_snet = models.Social_Network(s_name=snamesocialnetwork)
    db.add(db_snet)
    db.commit()
    db.refresh(db_snet)
    return db_snet


##################################################################################
############################ status ######################################
# def get_status_by_name(statusname: str):
#     db = SessionLocal()
#     return (
#         db.query(models.Status).filter(models.Status.status_name == statusname).first()
#     )


def get_status_by_id(idstatus: int):
    db = SessionLocal()
    return (
        db.query(models.Status.status_name).filter(models.Status.id == idstatus).first()
    )


# get status  0-limit
def get_status(skip: int = 0, limit: int = 10):
    db = SessionLocal()
    return db.query(models.Status).offset(skip).limit(limit).all()


# POST status ---  status()
# def create_status(stausname: schemas.StatusCreate):
#     db = SessionLocal()
#     db_status = models.Status(status_name=stausname.status_name)
#     db.add(db_status)
#     db.commit()
#     db.refresh(db_status)
#     return db_status


#######################################################################
############################ Identity ######################################
# get identity  0-limit
def get_identiy(skip: int = 0, limit: int = 10):
    db = SessionLocal()
    return db.query(models.Identity).offset(skip).limit(limit).all()


def get_identiy_by_name(s_name: str):
    db = SessionLocal()
    return db.query(models.Identity).filter(models.Identity.appuser == s_name).first()


def get_identiy_by_network(s_network: int):
    db = SessionLocal()
    list = []
    list = (
        db.query(models.Identity).filter(models.Identity.s_network == s_network).all()
    )
    return list


# get con filtro social network appuser
# def get_identiy_snetwork_appuser(s_network: int, appuser: str):
#     db = SessionLocal()
#     return (
#         db.query(models.Identity)
#         .filter(
#             models.Identity.s_network == s_network, models.Identity.appuser == appuser
#         )
#         .first()
#     )


# POST identity ---  tab --- , id_on_network: int
def create_identity_social_user(identity: schemas.IdentityCreate):
    db = SessionLocal()
    db_identity = models.Identity(**identity.dict())
    db.add(db_identity)
    try:
        db.commit()
        db.refresh(db_identity)
        return {"status": "success", "details": "Insert done!"}
    except IntegrityError as e:
        err_msg = "Errore: {}".format(e.__str__())
        return {"status": "failure", "text": str(err_msg)}


# PUT identiy ----
def update_identity_social_user(
    s_network: int, appuser: str, identity: schemas.IdentityUpdate
):
    db = SessionLocal()
    identity_query = db.query(models.Identity).filter(
        models.Identity.s_network == s_network, models.Identity.appuser == appuser
    )
    db_idetity = identity_query.first()
    if not db_idetity:
        raise ValueError(
            f"Nessun dato nella tabella identity per questo networkid: {s_network} e user {appuser}"
        )
    update_data = identity.dict(exclude_unset=True)
    identity_query.filter(
        models.Identity.s_network == s_network, models.Identity.appuser == appuser
    ).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_idetity)
    return {"status": "success", "details": "Update done!"}


# DELETE identity ---
def delete_identity_social_user(s_network: int, appuser: str):
    db = SessionLocal()
    identity_query = db.query(models.Identity).filter(
        models.Identity.s_network == s_network, models.Identity.appuser == appuser
    )
    db_idetity = identity_query.first()
    if not db_idetity:
        raise ValueError(
            f"Nessun dato nella tabella identity per questo networkid: {s_network} e user {appuser}"
        )
    identity_query.delete(synchronize_session=False)
    db.commit()
    return {"status": "success", "details": "Delete done!"}


#############FINE IDENTITY ################################
############################ Setting ######################################
# POST setting ---  tab --- s_network: int  appuser:str     key : str    value: str
def create_setting_social_user(setting: schemas.SettingCreate):
    db = SessionLocal()
    db_setting = models.Setting(**setting.dict())
    db.add(db_setting)
    try:
        db.commit()
        db.refresh(db_setting)
        return {"status": "success"}
    except IntegrityError as e:
        return {"status": "failure", "text": f"Errore: {e}"}


# PUT
def update_setting(setting: schemas.SettingUpdate):
    db = SessionLocal()
    db_setting = (
        db.query(models.Setting)
        .filter_by(
            s_network=setting.s_network, appuser=setting.appuser, key=setting.key
        )
        .first()
    )
    if not db_setting:
        raise ValueError(
            f"No data found for network ID {setting.s_network} and user {setting.appuser}"
        )

    # update_data = setting.dict(exclude_unset=True)
    for key, value in setting:
        setattr(db_setting, key, value)
    try:
        db.commit()
        db.refresh(db_setting)
        return {"status": "success", "details": "Update done!"}
    except IntegrityError as e:
        return ValueError(str(e))


# GET
def get_settings(uname_on_snet: str, snet_id: int = 1):
    db = SessionLocal()
    query = []
    query = (
        db.query(models.Setting)
        .filter(
            models.Setting.s_network == snet_id, models.Setting.appuser == uname_on_snet
        )
        .all()
    )

    # .first()
    return {i.key: i.value for i in query}


# def get_setting_by_name_key(s_network: int, s_name: str, s_key: str):
#     db = SessionLocal()
#     query = (
#         db.query(models.Setting)
#         .filter(
#             models.Setting.s_network == s_network,
#             models.Setting.appuser == s_name,
#             models.Setting.key == s_key,
#         )
#         .all()
#     )
#     return query


def delete_setting_by_key(setting: schemas.SettingDelete):
    db = SessionLocal()
    db_setting = (
        db.query(models.Setting)
        .filter_by(
            s_network=setting.s_network, appuser=setting.appuser, key=setting.key
        )
        .first()
    )
    if not db_setting:
        raise ValueError(
            f"No data found for network ID {setting.s_network}, user {setting.appuser}, and key {setting.key}"
        )

    db.delete(db_setting)
    db.commit()
    return {"status": "success", "details": "Delete done!"}


#####################################POST######################


# get con filtro  status post
def get_post_by_id(post_id: int) -> Optional[models.Post]:
    db = SessionLocal()
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def get_post_by_status(
    user: str = "", status: Optional[int] = None
) -> List[models.Post]:
    db = SessionLocal()
    q = db.query(models.Post)
    if user:
        q = q.filter(models.Post.author == user)
    if status:
        q = q.filter(models.Post.status == status)

    return q.all()


# get all post senza filtro con max visualizzazione di 10
def get_post() -> List[models.Post]:
    db = SessionLocal()
    return db.query(models.Post).filter(models.Post.status == 2).all()


# get all post filter by s_network
# def get_post_by_snet(snet: int):
#     db = SessionLocal()
#     return (
#         db.query(models.Post)
#         .filter(models.Post.status == 2, models.Post.s_network == snet)
#         .all()
#     )


# POST post ---  tab --- , id_on_network: int
def create_post_social_user(
    post_content: str,
    user: str,
    pathimages: List[str] = [],
    sched_date: Optional[date] = None,
    s_net: int = 1,
):
    db = SessionLocal()
    # 1) se c'è immagine prima devo inseire path immagine nel db
    if not sched_date:
        status_init = 1
    else:
        status_init = 2

    post = schemas.PostCreate(
        s_network=s_net,
        id_on_network="",
        content=post_content,
        creation_date=date.today(),
        scheduling_date=sched_date,
        publication_date=None,
        status=status_init,
        author=user,
    )

    db_post = models.Post(**post.dict())
    db.add(db_post)
    try:
        db.commit()
        newid = db_post.id
        db.refresh(db_post)
        # se presente inserisco immagine nel database e associo id del post appena creato
        for pathimage in pathimages:
            create_image(db=db, path=pathimage, post_id=newid)
        db.commit()
        return {"status": "success", "details": "Insert post in db done!"}
    except IntegrityError as e:
        err_msg = "Errore: {}".format(e.__str__())
        return {"status": "failure", "text": str(err_msg)}


def reflect_post_social_user(
    id_on_network: str,
    post_content: str,
    pathimage: List[str],
    publ_date: date,
    user: str,
    s_net: int = 1,
):
    db = SessionLocal()

    if get_post_by_snid(db, id_on_network, snet_id=s_net):
        return {"status": "failure", "details": "Post already exists in DB"}

    status_published = 3
    post = schemas.PostCreate(
        s_network=s_net,
        id_on_network=id_on_network,
        content=post_content,
        creation_date=date.today(),
        scheduling_date=date.today(),
        publication_date=publ_date,
        status=status_published,
        author=user,
    )

    db_post = models.Post(**post.dict())
    db.add(db_post)
    newid = db_post.id
    # se presente inserisco immagine nel database e associo id del post appena creato
    for p in pathimage:
        db_image = models.Image(path=p, post=newid)
        db.add(db_image)
    try:
        db.commit()
        db.refresh(db_post)
        return {"status": "success", "details": "Insert post in db done!"}
    except IntegrityError as e:
        err_msg = "Errore: {}".format(e.__str__())
        return {"status": "failure", "text": str(err_msg)}


# PUT ---- verificare se funziona todo
def update_post(
    idpost: int, post_content: str, status_post: int, sched_date: Optional[date] = None
):
    db = SessionLocal()
    db_post = db.query(models.Post).get(idpost)
    if not db_post:
        raise ValueError(
            f"Nessun dato nella tabella identity per questo post: {idpost}."
        )
    if post_content:
        db.query(models.Post).filter(models.Post.id == idpost).update(
            {
                "status": int(status_post),
                "content": str(post_content),
                "scheduling_date": sched_date,
            },
            synchronize_session=False,
        )
    else:
        db.query(models.Post).filter(models.Post.id == idpost).update(
            {"status": int(status_post), "scheduling_date": sched_date},
            synchronize_session=False,
        )
    db.commit()
    return {"status": "success", "details": "Post {idpost} - Update done!"}


# DELETE post ---
def delete_post(idpost: int):
    db = SessionLocal()
    post = (
        db.query(models.Post)
        .filter(models.Post.id == idpost, models.Post.status.in_([1, 2]))
        .first()
    )

    if not post:
        raise ValueError(
            f"Nessun dato oppure stato>2 nella tabella post per idpost= {idpost}"
        )

    db.query(models.Post).filter(models.Post.id == idpost).delete(
        synchronize_session=False
    )

    db.query(models.Image).filter(models.Image.post == idpost).delete(
        synchronize_session=False
    )

    db.commit()
    return {"status": "success", "details": f"Post {idpost} - Delete done!"}


#############FINE POST ################################
################## inserire le risposte ai tweet ##############
def insert_answer_post(
    idpost: int,
    content: str,
    author: str,
    id_on_network: str,
    publication_date: Optional[date] = None,
    reply_to=None,
):
    db = SessionLocal()
    post = (
        db.query(models.Post.id, models.Post.publication_date)
        .filter(models.Post.id == idpost)
        .first()
    )
    id_post = post[0]

    if publication_date is None:
        publication_date = post[1]

    db_answer = models.Answer(
        post=id_post,
        content=content,
        author=author,
        id_on_network=id_on_network,
        publication_date=publication_date,
        reply_to=reply_to,
    )
    db.add(db_answer)
    try:
        db.commit()
        newid = db_answer.id
        print(newid)
        db.refresh(db_answer)
        return {"status": "success", "details": "Insert answer in db done!"}
    except IntegrityError as e:
        err_msg = "Errore: {}".format(e.__str__())
        print(err_msg)
        return {"status": "failure", "text": str(err_msg)}


def get_answer_post(idpost: int):
    db = SessionLocal()
    return db.query(models.Answer).filter(models.Answer.post == idpost).all()


# DELETE answer ---
def delete_answer(idpost: int) -> Dict[str, str]:
    db = SessionLocal()
    answer_query = db.query(models.Answer).filter(models.Answer.post == idpost)
    count = answer_query.count()
    if count > 0:
        answer_query.delete(synchronize_session=False)
        db.commit()
    return {"status": "success", "details": "Delete done!"}


# Put aggiornameto parziale solo lo stato e id del post su twitter     date.today()
def update_post_status_id_on_network(
    idpost: int, status: int, id_on_net: str
) -> Dict[str, str]:
    db = SessionLocal()
    db.query(models.Post).filter(models.Post.id == idpost).update(
        {
            "status": int(status),
            "id_on_network": id_on_net,
            "publication_date": str(date.today()),
        },
        synchronize_session=False,
    )
    db.commit()
    return {"status": "success", "details": "Post {idpost} - Update done!"}


def get_images_for_post(idpost: int) -> List[str]:
    db = SessionLocal()
    return db.query(models.Image.path).filter(models.Image.post == idpost).all()
