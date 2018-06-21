import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

from keras.layers import Embedding
from gensim.models import Word2Vec
from utils.text_utils import tokenize
from utils.math_utils import create_oh_vector
from utils.logging import log, log_error
import numpy as np


class WordEmbeddings:
    EMPTY = 'EMP'
    UNKNOWN = 'unknown'

    def __init__(self, model):
        self.model = model
        self.size = len(model.wv.vocab) + 1
        self.oh_dict = {}
        log('WordEmbeddings created')

    @staticmethod
    def from_file(filename):
        log(f'loading WordEmbeddings from file {filename}')
        model = Word2Vec.load(filename)
        return WordEmbeddings(model)

    @staticmethod
    def from_sentences(sentences, size=25, window=5, min_count=1):
        log('creating new WordEmbeddings from text')
        processes_sentences = tokenize(sentences)
        model = Word2Vec(processes_sentences, size=size, window=window, min_count=min_count)
        return WordEmbeddings(model)

    def sentences_to_indices(self, sentences):
        processes_sentences = tokenize(sentences)
        return np.array([[self.get_index(word) for word in sentence] for sentence in processes_sentences])

    def sentences_to_oh(self, sentences):
        processes_sentences = tokenize(sentences)
        return np.array([[self.get_oh(word) for word in sentence] for sentence in processes_sentences])

    def info(self):
        log(f'number of word vectors: {self.size}')

    def save(self, filename):
        log(f'saving word embeddings to {filename}')
        self.model.init_sims(replace=True)
        self.model.save(filename)

    def keras_embeddings_layer(self):
        # vocab_len = len(self.model.wv.vocab)
        # emb_dim = self.model.wv.vector_size
        # emb_matrix = self.model.wv.syn0
        # embedding_layer = Embedding(vocab_len, emb_dim, trainable=False)
        # embedding_layer.build((None,))
        # embedding_layer.set_weights([emb_matrix])
        # return embedding_layer
        return self.model.wv.get_keras_embedding()

    def get_index(self, word):
        try:
            return self.model.wv.vocab[word].index
        except Exception as error:
            log_error(f'unknown word {word}')
            return self.model.wv.vocab[WordEmbeddings.UNKNOWN].index

    def get_word(self, index):
        assert index < self.size, 'index is greater than vocab size'
        return self.model.wv.index2word[index]

    def get_vector(self, word):
        return self.model.wv[word]

    def get_oh(self, word):
        if word not in self.oh_dict:
            index = self.get_index(word)
            self.oh_dict[word] = create_oh_vector(index, self.size)
        return self.oh_dict[word]

    def get_word_for_oh(self, oh_encoding):
        assert oh_encoding.shape[0] == self.size, f'must have a size of {self.size}'
        index = np.argmax(oh_encoding)
        return self.get_word(index)

    def ohs_to_sentence(self, ohs):
        assert len(ohs.shape) == 2, 'must be an array of ohs'
        words = [self.get_word_for_oh(oh) for oh in ohs]
        return ' '.join(words)

    def indexes_to_sentence(self, indexes):
        words = [self.get_word(index) for index in indexes]
        return ' '.join(words)