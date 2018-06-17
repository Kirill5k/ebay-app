from mongoengine import *
from datetime import datetime
from config import Config


connect(db=Config.mongo['db'], username=Config.mongo['username'], password=Config.mongo['password'], host=Config.mongo['host'])


class Price(EmbeddedDocument):
    sell = StringField()
    cash = StringField()
    exchange = StringField()


class Query(EmbeddedDocument):
    string = StringField()
    date = DateTimeField(default=datetime.utcnow)


class CexPhone(Document):
    name = StringField()
    query = EmbeddedDocumentField(Query)
    price = EmbeddedDocumentField(Price)
    meta = {'collection': 'cex-listings'}