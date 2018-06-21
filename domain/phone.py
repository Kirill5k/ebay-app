from mongoengine import EmbeddedDocument, StringField
from nlp.embeddings import WordEmbeddings


class PhoneDetails(EmbeddedDocument):
    brand = StringField(default=WordEmbeddings.UNKNOWN)
    model = StringField(default=WordEmbeddings.UNKNOWN)
    memory = StringField(default=WordEmbeddings.UNKNOWN)
    network = StringField(default=WordEmbeddings.UNKNOWN)
    color = StringField(default=WordEmbeddings.UNKNOWN)
    year = StringField(default=WordEmbeddings.UNKNOWN)

    def __str__(self):
        summary = [self.brand, self.model, self.memory, self.year, self.color, self.network]
        summary = ' '.join([item for item in summary if item is not WordEmbeddings.UNKNOWN]).strip()
        return summary if len(summary) > 0 else WordEmbeddings.UNKNOWN