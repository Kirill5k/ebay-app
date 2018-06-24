from clients.ebay.ebay_client import EbayClient
from nlp.Seq2SeqPredictor import Seq2SeqPredictor
from nlp.embeddings import WordEmbeddings
from config import Config
from utils.logging import Logger
from domain.ebay import EbayPhone
from typing import List


class EbayService:
    logger = Logger.of('EbayService')
    client = EbayClient()
    predictor = Seq2SeqPredictor.from_file(Config.get_filepath('predictor-model'), Config.get_filepath('predictor-weights'))
    embeddings = WordEmbeddings.from_file(Config.get_filepath('word2vec'))

    @classmethod
    def get_latest_phones(cls) -> List[EbayPhone]:
        phones = cls.client.get_latest_phones()
        for phone in phones:
            phone.formatted_title = cls.__get_formatted_title(phone)
            cls.__save(phone)
        return phones

    @classmethod
    def __get_formatted_title(cls, phone: EbayPhone):
        try:
            return cls.__format_title(phone.title)
        except Exception as error:
            cls.logger.error(f'error processing phone "{phone.title}": {error}')
            return WordEmbeddings.UNKNOWN

    @classmethod
    def __format_title(cls, ebay_title: str) -> str:
        indexes = cls.embeddings.sentences_to_indices([ebay_title])
        prediction_ohs = cls.predictor.predict(indexes)[0]
        prediction = cls.embeddings.ohs_to_sentence(prediction_ohs)
        return prediction.replace(WordEmbeddings.UNKNOWN, '').replace(WordEmbeddings.EMPTY, '').strip()

    @classmethod
    def __save(cls, phone):
        try:
            phone.save()
        except Exception as error:
            cls.logger.error(f'unable to save: {error}')