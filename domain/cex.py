from mongoengine import *
from datetime import datetime
from config import Config
from domain.phone import PhoneDetails


connect(db=Config.mongo['db'], username=Config.mongo['username'], password=Config.mongo['password'], host=Config.mongo['host'])


class Price(EmbeddedDocument):
    sell = FloatField()
    cash = FloatField()
    exchange = FloatField()


class Query(EmbeddedDocument):
    string = StringField()
    date = DateTimeField(default=datetime.utcnow)


class CexPhone(Document):
    name = StringField()
    condition = StringField()
    details = EmbeddedDocumentField(PhoneDetails)
    query = EmbeddedDocumentField(Query)
    price = EmbeddedDocumentField(Price)
    meta = {'collection': 'cex-listings'}
