from sqlalchemy import Boolean, Integer, String, Text  # type: ignore
from sqlalchemy import Column, ForeignKey  # type: ignore
from sqlalchemy.types import Date  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

# from sqlalchemy.sql import func
from .database import Base


class AppUser(Base):
    __tablename__ = "appuser"  # "users"
    __table_args__ = {"schema": "socialcampaigns"}

    username = Column(String, primary_key=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    identity = relationship("Identity", back_populates="appuser_rel")
    setting = relationship("Setting", back_populates="appuser_rel")


class Social_Network(Base):
    __tablename__ = "social_network"
    __table_args__ = {"schema": "socialcampaigns"}

    id = Column(Integer, primary_key=True)
    s_name = Column(String, unique=True, index=True)

    identity = relationship("Identity", back_populates="s_network_rel")
    setting = relationship("Setting", back_populates="s_network_rel")
    post = relationship("Post", back_populates="s_network_rel")


class Status(Base):
    __tablename__ = "status"
    __table_args__ = {"schema": "socialcampaigns"}
    id = Column(Integer, primary_key=True)
    status_name = Column(String, unique=True, index=True)

    post = relationship("Post", back_populates="status_rel")


class Identity(Base):
    __tablename__ = "identity"
    __table_args__ = {"schema": "socialcampaigns"}
    s_network = Column(
        Integer, ForeignKey("socialcampaigns.social_network.id"), primary_key=True
    )
    appuser = Column(
        String, ForeignKey("socialcampaigns.appuser.username"), primary_key=True
    )
    id_on_network = Column(String)

    # relationship provided by SQLAlchemy ORM
    s_network_rel = relationship("Social_Network", back_populates="identity")
    appuser_rel = relationship("AppUser", back_populates="identity")


class Setting(Base):
    __tablename__ = "setting"
    __table_args__ = {"schema": "socialcampaigns"}
    s_network = Column(
        Integer, ForeignKey("socialcampaigns.social_network.id"), primary_key=True
    )
    appuser = Column(
        String, ForeignKey("socialcampaigns.appuser.username"), primary_key=True
    )
    key = Column(String, primary_key=True)
    value = Column(String)

    # relationship provided by SQLAlchemy ORM
    s_network_rel = relationship("Social_Network", back_populates="setting")
    appuser_rel = relationship("AppUser", back_populates="setting")

    def __repr__(self):
        return f'Setting(s_network={self.s_network}, appuser="{self.appuser}", key="{self.key}", value="{self.value}")'


class Post(Base):
    __tablename__ = "post"
    __table_args__ = {"schema": "socialcampaigns"}
    id = Column(Integer, primary_key=True)
    s_network = Column(Integer, ForeignKey("socialcampaigns.social_network.id"))
    id_on_network = Column(String)
    content = Column(String)
    creation_date = Column(Date)
    scheduling_date = Column(Date)
    publication_date = Column(Date)
    status = Column(Integer, ForeignKey("socialcampaigns.status.id"))
    author = Column(String, ForeignKey("socialcampaigns.appuser.username"))

    status_rel = relationship("Status", back_populates="post")
    s_network_rel = relationship("Social_Network", back_populates="post")
    image = relationship("Image", back_populates="post_rel")
    answer = relationship("Answer", back_populates="post_rel")


class Image(Base):
    __tablename__ = "image"
    __table_args__ = {"schema": "socialcampaigns"}
    id = Column(Integer, primary_key=True)
    path = Column(String)
    post = Column(Integer, ForeignKey("socialcampaigns.post.id"))
    id_on_network = Column(String, nullable=True)

    post_rel = relationship("Post", back_populates="image")


class Answer(Base):
    __tablename__ = "answer"
    __table_args__ = {"schema": "socialcampaigns"}

    id = Column(String, primary_key=True)
    post = Column(Integer, ForeignKey("socialcampaigns.post.id"))
    content = Column(Text)
    author = Column(String)
    id_on_network = Column(String)
    publication_date = Column(Date, nullable=True)
    reply_to = Column(String)

    post_rel = relationship("Post", back_populates="answer")


# content=Column(String)
