from mongoengine import *
from datetime import datetime
from config import Config
from domain.phone import PhoneDetails


connect(db=Config.mongo['db'], username=Config.mongo['username'], password=Config.mongo['password'], host=Config.mongo['host'])


class Seller(EmbeddedDocument):
    name = StringField()
    feedback_score = IntField()
    feedback_percentage = FloatField()


class EbayPhone(Document):
    id = StringField(required=True, primary_key=True)
    title = StringField()
    formatted_title = StringField()
    price = FloatField()
    images = ListField(URLField())
    details = EmbeddedDocumentField(PhoneDetails)
    seller = EmbeddedDocumentField(Seller)
    condition = StringField()
    url = URLField(unique=True)
    date_posted = DateTimeField(default=datetime.utcnow)
    network = StringField()
    meta = {'collection': 'ebay-listings'}
