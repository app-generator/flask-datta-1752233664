# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Members(db.Model):

    __tablename__ = 'Members'

    id = db.Column(db.Integer, primary_key=True)

    #__Members_FIELDS__
    full_name = db.Column(db.String(255),  nullable=True)
    phone_number = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    #__Members_FIELDS__END

    def __init__(self, **kwargs):
        super(Members, self).__init__(**kwargs)


class Groups(db.Model):

    __tablename__ = 'Groups'

    id = db.Column(db.Integer, primary_key=True)

    #__Groups_FIELDS__
    cycle_year = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    name = db.Column(db.String(255),  nullable=True)

    #__Groups_FIELDS__END

    def __init__(self, **kwargs):
        super(Groups, self).__init__(**kwargs)


class Aliases(db.Model):

    __tablename__ = 'Aliases'

    id = db.Column(db.Integer, primary_key=True)

    #__Aliases_FIELDS__
    alias_name = db.Column(db.String(255),  nullable=True)

    #__Aliases_FIELDS__END

    def __init__(self, **kwargs):
        super(Aliases, self).__init__(**kwargs)


class Contributions(db.Model):

    __tablename__ = 'Contributions'

    id = db.Column(db.Integer, primary_key=True)

    #__Contributions_FIELDS__
    week_number = db.Column(db.Integer, nullable=True)
    amount = db.Column(db.Integer, nullable=True)
    date_paid = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(255),  nullable=True)

    #__Contributions_FIELDS__END

    def __init__(self, **kwargs):
        super(Contributions, self).__init__(**kwargs)


class Payout_Schedule(db.Model):

    __tablename__ = 'Payout_Schedule'

    id = db.Column(db.Integer, primary_key=True)

    #__Payout_Schedule_FIELDS__
    week_number = db.Column(db.Integer, nullable=True)
    amount_expected = db.Column(db.String(255),  nullable=True)
    date_paid = db.Column(db.DateTime, default=db.func.current_timestamp())
    notes = db.Column(db.Text, nullable=True)

    #__Payout_Schedule_FIELDS__END

    def __init__(self, **kwargs):
        super(Payout_Schedule, self).__init__(**kwargs)



#__MODELS__END
