import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Message(SqlAlchemyBase):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True)

    text = sqlalchemy.Column(sqlalchemy.String,
                             nullable=False)

    sender_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('users.id'))

    receiver_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey('users.id'))

    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
