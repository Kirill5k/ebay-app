from domain.ebay import EbayPhone
from domain.phone import PhoneDetails
import pandas as pd
import numpy as np
from utils.text_utils import match_word, tokenize, update_vocabulary
from utils.logging import log
from nlp.embeddings import WordEmbeddings
from nlp.training import DataSet
from config import Config


def create_embeddings():
    titles = pd.read_csv(Config.get_filepath('train-data'))['title'].tolist()
    titles = ['EMP ' + title + ' EMP' for title in titles]
    embeddings = WordEmbeddings.from_sentences(titles)
    embeddings.save(Config.get_filepath('word2vec'))


def clean_phones():
    log('cleaning phones')
    EbayPhone.objects().update(details=PhoneDetails())
    for phone in EbayPhone.objects(title__contains='*'):
        phone.update(title=phone.title.replace('*', ' '))
    for phone in EbayPhone.objects(title__contains='/'):
        phone.update(title=phone.title.replace('/', ' '))
    for phone in EbayPhone.objects(title__contains='+'):
        phone.update(title=phone.title.replace('+', ' plus '))


def set_manufacturer():
    log('setting manufacturer')
    brands = pd.read_csv(Config.get_filepath('brands'))
    for index, row in brands.iterrows():
        spelling, brand = row['spelling'], row['brand']
        EbayPhone.objects(title=match_word(spelling)).update(set__details__brand=brand)


def set_model():
    log('setting model')
    models = pd.read_csv(Config.get_filepath('models'))
    for index, row in models.iterrows():
        brand, spelling, model = row['brand'], row['spelling'], row['model']
        EbayPhone.objects(details__brand=brand, title=match_word(spelling)).update(set__details__model=model)


def set_operator():
    log('setting operator')
    operators = pd.read_csv(Config.get_filepath('operators'))
    for index, row in operators.iterrows():
        brand, network = row['brand'], row['network']
        EbayPhone.objects(title=match_word(brand)).update(set__details__network=network)


def set_color():
    log('setting color')
    colors = pd.read_csv(Config.get_filepath('colors'))
    for index, row in colors.iterrows():
        spelling, color = row['spelling'], row['color']
        EbayPhone.objects(title=match_word(spelling)).update(set__details__color=color)


def set_memory():
    log('setting memory')
    memory_sizes = pd.read_csv(Config.get_filepath('memory'))
    for index, row in memory_sizes.iterrows():
        spelling, size = row['spelling'], row['size']
        EbayPhone.objects(title=match_word(spelling)).update(set__details__memory=size)


def set_year():
    log('setting year')
    years = pd.read_csv(Config.get_filepath('years'))
    for index, row in years.iterrows():
        spelling, year = row['spelling'], row['year']
        EbayPhone.objects(title=match_word(spelling)).update(set__details__year=str(year))


def create_data_set():
    log('creating train data')
    phones = [[phone.title, phone.details.brand, phone.details.model, phone.details.color, phone.details.memory, phone.details.year, phone.details.network] for phone in EbayPhone.objects()]
    phones_array = np.array(phones)
    phones_df = pd.DataFrame(phones_array, columns=['title', 'brand', 'model', 'color', 'memory', 'year', 'network'])
    phones_df.to_csv(Config.get_filepath('train-data'), index=False)


def print_unknown_models():
    models = ['htc', 'motorola', 'samsung', 'apple', 'nokia', 'huawei', 'honor', 'microsoft', 'oneplus', 'meizu', 'google', 'lg']
    for model in models:
        for phone in EbayPhone.objects(details__brand=model, details__model='unknown'):
            print(phone.title)


# clean_phones()
# set_manufacturer()
# set_operator()
# set_color()
# set_model()
# set_memory()
# set_year()
# create_data_set()
# create_embeddings()
# print_unknown_models()

# titles = pd.read_csv('data/mobile-phone-titles.csv')['title'].tolist()
# titles = ['EMP ' +title + ' EMP' for title in titles]
emb = WordEmbeddings.from_file(Config.get_filepath('word2vec'))
# emb = WordEmbeddings.from_sentences(titles)
# emb.info()
# vocab = update_vocabulary(tokenize(titles))
dataset = DataSet(emb, Config.get_filepath('train-data'), y_labels=['brand', 'model', 'memory', 'color', 'network'])
