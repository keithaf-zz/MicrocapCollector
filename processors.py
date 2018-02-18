import numpy as np
import re


def StringProcessor(raw_data, indicies):
    for x in indicies:
        for i in range(0, len(raw_data[x])):
            temp = raw_data[x][i].strip()
            temp = re.sub("[^0-9.]", "", temp)
            if temp == "?" or temp == "Low Vol" or temp == "":
                temp = 0
            else:
                temp = float(temp)
            raw_data[x][i] = temp
    return raw_data


def MCProcessor(raw_data):
    np_market_cap = np.asarray(raw_data[2], dtype=float)
    greater_than = np.argwhere(np_market_cap < 50000000)
    for i in range(0, len(raw_data)):
        raw_data[i] = np.take(np.asarray(raw_data[i]), greater_than).tolist()
    return raw_data


def MCVProcessor(raw_data):
    np_market_cap = np.asarray(raw_data[2], dtype=float)
    np_volume = np.asarray(raw_data[3], dtype=float)
    ratios = []
    for x, y in zip(np.nditer(np_market_cap), np.nditer(np_volume)):
        if x == 0:
            ratios.append(0)
        else:
            ratios.append((y / x))
    np_ratios = np.asarray(ratios, dtype=float)
    mcv_ratios = np.argwhere(np_ratios <= 0.02)
    for i in range(0, len(raw_data)):
        raw_data[i] = np.take(np.asarray(raw_data[i]), mcv_ratios).tolist()
    return raw_data


def Flattener(raw_data):
    for i in range(0, len(raw_data)):
        arr = []
        for j in range(0, len(raw_data[i])):
            arr.append(raw_data[i][j][0])
        raw_data[i] = arr
    return raw_data


def CSTSProcessor(raw_data):
    supply = raw_data[1]
    if not 3 < len(supply) < 6:
        ratio = 0
    else:
        c_supply = float(supply[2])
        t_supply = float(supply[3])
        if c_supply == 0:
            ratio = 0
        else:
            ratio = c_supply / t_supply
    raw_data[1] = ratio
    return raw_data
