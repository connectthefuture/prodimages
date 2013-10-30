#!/usr/bin/env python

def calculateMovingAverage(prices, period):
    dates = list(prices.keys())
    dates.sort()
    total = 0.0
    count = 0
    average_dict = {}

    for i, d in enumerate(dates):
        # search through prior dates and eliminate any that are too old
        old = [e for e in dates[i-count:i] if (d-e).days > period]
        total -= sum(prices[o] for o in old)
        count -= len(old)

        # add in the current date
        total += prices[d]
        count += 1

        average_dict[d] = total / count

    return average_dict


import datetime as dt
from collections import deque
from itertools import tee, islice, izip

def dayiter(start, end):
    one = dt.timedelta(days=1)
    day = start
    while day <= end:
        yield day
        day += one

def moving_average(mapping, window, dft=0):
    n = float(window)
    t1, t2 = tee(dayiter(min(mapping), max(mapping)))
    s = sum(mapping.get(day, dft) for day in islice(t2, window))
    yield s / n
    for olddate, newdate in izip(t1, t2):
        oldvalue = mapping.get(olddate, dft)
        newvalue = mapping.get(newdate, dft)
        s += newvalue - oldvalue
        yield s / n
        
  