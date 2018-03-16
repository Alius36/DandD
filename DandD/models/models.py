# coding: utf-8
from DandD.utilities.exception import WrongInput, DuplicateValue
from sqlalchemy import BigInteger, Column, DateTime, Text, text, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


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
        if user is not None:
            dbsession.add(user)
        else:
            raise WrongInput

    @classmethod
    def get_all_username(cls, dbsession):
        return dbsession.query(User.username).all()

    @classmethod
    def get_user_by_username(cls, dbsession, username):
        return dbsession.query(User).filter(User.username == username).first()


# ROLE
class Role(Base):
    __tablename__ = 'role'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('role_id_seq'::regclass)"))
    value = Column(Text, nullable=False, unique=True)

    @classmethod
    def get_all_role(cls, dbsession):
        return dbsession.query(Role).all()

