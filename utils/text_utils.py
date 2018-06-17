from nltk.tokenize import word_tokenize
from collections import Counter
import numpy as np
import re


def max_len(sentences):
    return max(map(len, tokenize(sentences)))


def match_word(word):
    return re.compile(r'^(.*?(\b' + re.escape(str(word)) + r'\b)[^$]*)$')


def tokenize(sentences):
    regex = re.compile(r'^[^a-zA-Z0-9\\-]{1}$')
    is_valid_word = lambda word: not regex.match(word)
    return np.array([list(filter(is_valid_word, word_tokenize(sentence))) for sentence in sentences])


def update_vocabulary(processed_text, vocabulary=Counter()):
    for words in processed_text:
        vocabulary.update(words)
    return vocabulary
