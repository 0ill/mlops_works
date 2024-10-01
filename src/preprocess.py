import pandas as pd
import numpy as np
from lifetimes.utils import calibration_and_holdout_data 
from lifetimes.utils import summary_data_from_transaction_data

def bgf_data(start_data):
    data = summary_data_from_transaction_data(start_data, 'ID', 'Date','Amount', observation_period_end='2024-04-30',)
    data.to_csv('../data/bgf_data.csv')
    return data.head()

def ggf_data(start_data):
    data_cal_holdout = calibration_and_holdout_data(start_data, 'ID', 'Date',
                                        calibration_period_end='2024-04-01',
                                        observation_period_end='2024-05-30' )
    data_cal_holdout =data_cal_holdout[data_cal_holdout['frequency'] > 0]
    data_cal_holdout.to_csv('../data/bgf_data.csv')
    return data_cal_holdout.head()

df = pd.read_csv('../data/transactional_data.csv')
data = bgf_data(df)
data.head()
data = ggf_data(df)
data.head()
