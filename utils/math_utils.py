import numpy as np


def create_oh_vector(index, size):
    oh = np.zeros(size)
    oh[index] = 1
    return oh