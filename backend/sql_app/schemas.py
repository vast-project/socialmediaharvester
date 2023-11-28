from typing import List, Optional

from datetime import date

from pydantic import BaseModel


###################################################
#######class Answer(Base) :
class AnswerBase(BaseModel):
    content: str
    author: str
    id_on_network: str
    publication_date: Optional[date]
    reply_to: int

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


class AnswerCreate(AnswerBase):
    pass


class Answer(AnswerBase):
    id: int
    post: int

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


###################################################
#######class Image(Base) :
class ImageBase(BaseModel):
    path: str = ""


class ImageCreate(ImageBase):
    post: int


class Image(ImageBase):
    id: int

    class Config:
        orm_mode = True


###################################################
#######class Post(Base) :
class PostBase(BaseModel):
    s_network: int
    id_on_network: Optional[str]
    content: str
    creation_date: date
    scheduling_date: Optional[date]
    publication_date: Optional[date]
    status: int
    author: str

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    # status:int
    image: List[Image] = []
    answer: List[Answer] = []

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


class PostDelete(BaseModel):
    id: int

    class Config:
        orm_mode = True


""" class PostUpdate(BaseModel):
    content:str
    scheduling_date:Optional[date]
    status:int
    class Config:
        orm_mode = True    """


###################################################
#######class Status(Base) :
class StatusBase(BaseModel):
    status_name: str


# le seguenti classi ereditano Social_NetworkBase
class StatusCreate(StatusBase):
    pass


class Status(StatusBase):
    id: int
    post: List[Post] = []

    class Config:
        orm_mode = True


# la status ha una relazione con i post status_post=relationship("Post",back_populates="status_rel")


###################################################
#######class Identity(Base) :
class IdentityBase(BaseModel):
    id_on_network: str


class Identity(IdentityBase):
    s_network: int
    appuser: str

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


# le seguenti classi ereditano Social_NetworkBase
class IdentityCreate(Identity):
    pass

    class Config:
        orm_mode = True


class IdentityUpdate(IdentityBase):
    # id_on_network: Optional[str]

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


class IdentityDelete(BaseModel):
    s_network: int
    appuser: str

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


# la tabella identity ha due relazioni con social_network e appuser


###################################################
#######class Setting(Base) :
class SettingBase(BaseModel):
    key: str
    value: str

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


class Setting(SettingBase):
    s_network: int
    appuser: str

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


# le seguenti classi ereditano Social_NetworkBase
class SettingCreate(Setting):
    pass

    class Config:
        anystr_strip_whitespace = True
        orm_mode = True


class SettingUpdate(BaseModel):
    s_network: Optional[int] = None
    appuser: Optional[str] = None
    key: Optional[str] = None
    value: Optional[str] = None

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


class SettingDelete(BaseModel):
    s_network: int
    appuser: str
    key: str

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


""" class SettingCreate(SettingBase):
    key : str
    value: str """


###################################################
#######class Social_Network(Base) :
class Social_NetworkBase(BaseModel):
    s_name: str


# le seguenti classi ereditano Social_NetworkBase
class Social_NetworkCreate(Social_NetworkBase):
    pass


class Social_Network(Social_NetworkBase):
    id: int
    identity: List[Identity] = []
    setting: List[Setting] = []
    post: List[Post] = []

    class Config:
        orm_mode = True
        """Extra configuration options"""
        anystr_strip_whitespace = True  # remove trailing whitespace


###################################################
#######class User insert in appuser ##################


class UserBase(BaseModel):
    username: str


# le seguenti classi ereditano UserBase
class UserCreate(UserBase):
    password: str


class User(UserBase):
    is_active: bool
    identity: List[Identity] = []
    setting: List[Setting] = []

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True  # remove trailing whitespace
