"""Reusable queries without session management.
If a routine needs to handle its own session,
rather put it in persistence.py"""


from sqlalchemy.orm import Session  # type: ignore

from . import models, schemas


################################IMAGE
# post imate ---  add user
def create_image(db: Session, path: str, post_id: str) -> models.Image:
    db_image = models.Image(path=path, post=post_id)
    db.add(db_image)
    # db.refresh(db_image)
    return db_image


#####################################POST######################


def create_post_poll(db: Session, post: schemas.PostCreate):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    return {"status": "success", "details": "Insert post poll in db done!"}
    # try:
    #     # newid=db_post.id
    #     # db.refresh(db_post)

    # except IntegrityError as e:
    #     err_msg = "Errore: {}".format(e.__str__())
    #     return {"status": "failure", "text": str(err_msg)}


def get_post_by_snid(db: Session, id_on_snet: str, snet_id: int = 1) -> models.Post:
    return (
        db.query(models.Post)
        .filter(
            models.Post.id_on_network == id_on_snet, models.Post.s_network == snet_id
        )
        .first()
    )


def get_user_by_name(db: Session, user: str) -> models.AppUser:
    return db.query(models.AppUser).filter(models.AppUser.username == user).first()
