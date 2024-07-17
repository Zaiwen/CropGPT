import pandas as pd
import numpy as np
import re
from collections import Counter


# 导入词表
vocab = {'A': [1, 0, 0, 0], 'G': [0, 1, 0, 0], 'C': [0, 0, 1, 0], 'T': [0, 0, 0, 1]}
def coding(data_i):
    gotdata = []
    for snpi in data_i:
        gotdata.append(vocab.get(snpi))
    gotdata = np.expand_dims(np.array(gotdata).T, axis=0)
    # print(gotdata.shape)
    return gotdata

if __name__ == "__main__":
    A = "ACGT"*1500
    coding(A)