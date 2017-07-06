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
    if len(arr_no_none1) == 1 or len(arr_no_none1) == 0:
        return False, False

    return pearsonr(arr_no_none1, arr_no_none2)

if __name__ == '__main__':
    A, B = [1, 2, 4, 4], [0.1,0.22,0.112,0.4]
    result = calc_pearsonr(A, B)
    print(result)
    # print(None in [1,2,3,4,None])
    # print(corr(A, B))