import pandas as pd
import numpy as np
from lifetimes import BetaGeoFitter 
from lifetimes import GammaGammaFitter

def bgf_train():
    df = pd.read_csv('data/bgf_data.csv').set_index('ID')
    bgf = BetaGeoFitter(penalizer_coef=3.001)
    bgf.fit(df['frequency'], df['recency'], df['T'])
    bgf.save_model('models/bgf_small_size.pkl', save_data=False, save_generate_data_method=False)
    print(bgf)
    return bgf

def ggf_train():
    df = pd.read_csv('data/bgf_data.csv').set_index('ID')
    ggf = GammaGammaFitter(penalizer_coef = 10.)
    ggf.fit(df['frequency'],df['monetary_value'])
    ggf.save_model('models/ggf_small_size.pkl', save_data=False, save_generate_data_method=False)
    print(ggf)
    return ggf

bgf_model = bgf_train()
ggf_model = ggf_train()