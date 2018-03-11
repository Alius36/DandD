# coding: utf-8
from DandD.utilities.exception import WrongInput, DuplicateValue
from sqlalchemy import BigInteger, Column, DateTime, Text, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('user_id_seq'::regclass)"))
    nome = Column(Text, nullable=False)
    cognome = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    url_image = Column(Text)
    iscrizione_dt = Column(DateTime, nullable=False)
    username = Column(Text, unique=True)

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
