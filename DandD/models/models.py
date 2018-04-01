# coding: utf-8
import logging

from DandD.utilities.exception import WrongInput
from sqlalchemy import BigInteger, Column, DateTime, Text, text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata

logger = logging.getLogger(__name__)


# USER
class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('user_id_seq'::regclass)"))
    nome = Column(Text, nullable=False)
    cognome = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    url_image = Column(Text)
    iscrizione_dt = Column(DateTime, nullable=False)
    username = Column(Text, unique=True)
    fk_role_id = Column(ForeignKey(u'role.id', ondelete=u'RESTRICT', onupdate=u'CASCADE'), nullable=False,
                        server_default=text("nextval('user_fk_role_id_seq'::regclass)"))

    fk_role = relationship(u'Role')

    def __init__(self, dict_data):
        if dict_data is not None:
            for key in dict_data:
                setattr(self, key, dict_data[key])
        else:
            raise WrongInput

    @classmethod
    def insert_new_user(cls, dbsession, user):
        try:
            if user is not None:
                dbsession.add(user)
            else:
                raise WrongInput
        except Exception, e:
            logger.error(e)
            raise WrongInput

    @classmethod
    def get_all_username(cls, dbsession):
        return dbsession.query(User.username).all()

    @classmethod
    def get_user_by_username(cls, dbsession, username):
        return dbsession.query(User).filter(User.username == username).first()

    @classmethod
    def get_user_by_id(cls, dbsession, id):
        return dbsession.query(User).filter(User.id == id).first()


# ROLE
class Role(Base):
    __tablename__ = 'role'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('role_id_seq'::regclass)"))
    value = Column(Text, nullable=False, unique=True)

    @classmethod
    def get_all_role(cls, dbsession):
        return dbsession.query(Role).all()


# MANUAL
class Manual(Base):
    __tablename__ = 'manual'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('manual_id_seq'::regclass)"))
    title = Column(Text, nullable=False, unique=True)
    path = Column(Text, nullable=False, unique=True)
    upload_dt = Column(Text, nullable=False)
    fk_user = Column(ForeignKey(u'user.id', ondelete=u'RESTRICT', onupdate=u'CASCADE'), nullable=False,
                     server_default=text("nextval('manual_fk_user_seq'::regclass)"))

    user = relationship(u'User')

    def __init__(self, dict_data):
        if dict_data is not None:
            for key in dict_data:
                setattr(self, key, dict_data[key])
        else:
            raise WrongInput

    @classmethod
    def insert_new_manual(cls, dbsession, new_manual):
        try:
            if new_manual is not None:
                dbsession.add(new_manual)
            else:
                raise WrongInput
        except Exception, e:
            logger.error(e)
            raise WrongInput

    @classmethod
    def get_all_title(cls, dbsession):
        return dbsession.query(Manual.title).all()
