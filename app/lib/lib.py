from scipy.stats.stats import pearsonr

import numpy as np

"""
Perform two approaches for estimation and inference of a Pearson
correlation coefficient in the presence of missing data: complete case
analysis and multiple imputation.
"""


def corr(arr1, arr2):
    """Computes the Pearson correlation coefficient and a 95% confidence
    interval based on the data in X and Y."""


    X = []
    Y = []
    for index in range(len(arr1)):
        if arr1[index] == None or arr2[index] == None:
            continue
        X.append(arr1[index])
        Y.append(arr2[index])


    r = np.corrcoef(X, Y)[0,1]
    f = 0.5*np.log((1+r)/(1-r))
    se = 1/np.sqrt(len(X)-3)
    ucl = f + 2*se
    lcl = f - 2*se

    lcl = (np.exp(2*lcl) - 1) / (np.exp(2*lcl) + 1)
    ucl = (np.exp(2*ucl) - 1) / (np.exp(2*ucl) + 1)

    return r,lcl,ucl


def calc_pearsonr(arr1 ,arr2):
    if len(arr1) != len(arr2):
        print('Unequal length')
        return False, False
    arr_no_none1 = []
    arr_no_none2 = []
    for index in range(len(arr1)):
        if arr1[index] == None or arr2[index] == None:
            continue
        arr_no_none1.append(arr1[index])
        arr_no_none2.append(arr2[index])

    if len(arr_no_none1) <= 1 or len(arr_no_none2) <= 1:
        return False, False
    # print(arr_no_none1, arr_no_none2)
    return pearsonr(arr_no_none1, arr_no_none2)


def calc_rel_diff(obsList, predList):
    if len(obsList) != len(predList):
        return False

    arr_no_none1 = []
    arr_no_none2 = []
    for index in range(len(obsList)):
        if obsList[index] == None or predList[index] == None:
            continue
        arr_no_none1.append(obsList[index])
        arr_no_none2.append(predList[index])

    abs_diff = sum([abs(arr_no_none1[i] - arr_no_none2[i]) for i in range(len(arr_no_none2))])
    if len(arr_no_none2) == 0:
        return None, None
    avg_abs_diff = abs_diff / len(arr_no_none1)
    rel_diff = abs_diff / sum(arr_no_none1)

    return rel_diff, avg_abs_diff

def calc_abs_diff(obsList, predList):
    # hahaha
    if len(obsList) != len(predList):
        return False

    arr_no_none1 = []
    arr_no_none2 = []
    for index in range(len(obsList)):
        if obsList[index] == None or predList[index] == None:
            continue
        arr_no_none1.append(obsList[index])
        arr_no_none2.append(predList[index])

    abs_diff = sum([abs(arr_no_none1[i] - arr_no_none2[i]) for i in range(len(arr_no_none2))])
    if len(arr_no_none2) == 0:
        return None, None
    avg_abs_diff = abs_diff / len(arr_no_none1)
    rel_diff = abs_diff / sum(arr_no_none1)

    return avg_abs_diff, rel_diff
if __name__ == '__main__':
    A, B = [1, 2, None, 4], [1, 2, 7, 4]

    # print(None in [1,2,3,4,None])
    # print(corr(A, B))