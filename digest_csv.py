# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime

def get_year(date):
    return date.year

vget_year = np.vectorize(get_year)

def get_month(date):
    return date.month

vget_month = np.vectorize(get_month)

data = pd.read_csv(r"C:\Users\Duch Kraftu\Documents\MMWD\MMWD\AEP_hourly.csv")

dates = []
for index, date in enumerate(data['Datetime']):
    dates.append(datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))

dates = np.array(dates)
consumption = np.array(data['AEP_MW'])

consumption_dict = {}
for i in range(1, 13):
    timeframe = f'2016_{i}'
    power_usage = consumption[np.where((vget_year(dates) == 2016) & (vget_month(dates) == i))]
    consumption_dict.update({timeframe: power_usage})
    timeframe = f'2017_{i}'
    power_usage = consumption[np.where((vget_year(dates) == 2017) & (vget_month(dates) == i))]
    consumption_dict.update({timeframe: power_usage})
    timeframe = f'2018_{i}'
    power_usage = consumption[np.where((vget_year(dates) == 2018) & (vget_month(dates) == i))]
    consumption_dict.update({timeframe: power_usage})
    
for i in range(9,13):
    timeframe = f'2018_{i}'
    del(consumption_dict[timeframe])

for key, value in consumption_dict.items():
    np.savetxt(key + '.csv', value,)