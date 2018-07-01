import numpy as np
from functools import lru_cache


@lru_cache(maxsize=None)
def create_oh_vector(index, size):
    oh = np.zeros(size)
    oh[index] = 1
    return oh
