import pandas as pd
import numpy as np
from lifetimes.utils import calibration_and_holdout_data 
from lifetimes.utils import summary_data_from_transaction_data

def bgf_data(start_data):
    data1 = summary_data_from_transaction_data(start_data, 'ID', 'Date','Amount', observation_period_end='2024-04-30',)
    data1.reset_index().to_csv('data/bgf_data.csv')
    return data1.head()

def ggf_data(start_data):
    data2 = summary_data_from_transaction_data(start_data, 'ID', 'Date','Amount', observation_period_end='2024-04-30',)
    data2 =data2[data2['frequency'] > 0]
    data_cal_holdout = calibration_and_holdout_data(start_data, 'ID', 'Date',
                                        calibration_period_end='2024-04-01',
                                        observation_period_end='2024-05-30' )
    data_cal_holdout.reset_index().to_csv('data/ggf_data.csv')
    return data_cal_holdout.head()

df = pd.read_csv('data/transactional_data.csv')
data = bgf_data(df)
data.head()
data = ggf_data(df)
data.head()
