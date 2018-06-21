import pandas as pd
import numpy as np
from nlp.embeddings import WordEmbeddings
from sklearn.model_selection import train_test_split
from utils.text_utils import max_len
from keras.preprocessing.sequence import pad_sequences
from utils.logging import log


class DataSet:
    def __init__(self, embeddings: WordEmbeddings, data_file, x_label='title', y_labels=['brand']):
        self.data = pd.read_csv(data_file)
        self.embeddings = embeddings
        self.vocab_size = self.embeddings.size
        self.__prepare_x(x_label)
        self.__prepare_y(y_labels)
        log('DataSet created')

    def __prepare_x(self, x_label):
        log('preparing X')
        self.X_raw = self.data[x_label].values
        self.X_max_len = max_len(self.X_raw)
        indexed_sentences = self.embeddings.sentences_to_indices(self.X_raw)
        self.X_indexed = pad_sequences(indexed_sentences, self.X_max_len, dtype='int32')

    def __prepare_y(self, y_labels):
        log('preparing y')
        self.y_raw = [' '.join([row[label] for label in y_labels if row[label] is not 'unknown']) for index, row in self.data.iterrows()]
        self.y_max_len = max_len(self.y_raw)
        y_oh = self.embeddings.sentences_to_oh(self.y_raw)
        y_oh = [pad_sequences(y_oh_part, maxlen=self.y_max_len, padding='post', value=self.embeddings.get_oh('EMP')) for y_oh_part in np.array_split(y_oh,5)]
        self.y_oh = np.concatenate(y_oh)

    def get_all(self):
        return self.X_indexed, self.y_oh

    def get_train_test_data(self, test_size=0.2):
        '''
        :return: X_train, X_test, y_train, y_test
        '''
        return train_test_split(self.X_indexed, self.y_oh, test_size=test_size, random_state=42)