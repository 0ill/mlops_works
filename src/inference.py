import pandas as pd
import numpy as np
from lifetimes import BetaGeoFitter 
from lifetimes import GammaGammaFitter

def bgf_load(frequency,recency,T,t):
    bgf = BetaGeoFitter()
    bgf.load_model('models/bgf_small_size.pkl')
    cen = bgf.predict(t, frequency, recency, T)
    return cen

def ggf_load(frequency,recency,T, monetary_value):
    df = pd.DataFrame()
    df['frequency'] = frequency
    df['recency'] = recency
    df['T'] = T
    df['monetary_value'] = monetary_value
    ggf = GammaGammaFitter()
    ggf.load_model('models/ggf_small_size.pkl')
    bgf = BetaGeoFitter()
    bgf.load_model('models/bgf_small_size.pkl')
    CLT = ggf.customer_lifetime_value(
        bgf,
        df['frequency'],
        df['recency'],
        df['T'],
        df['monetary_value'],
        time=31, # months
        discount_rate=0.00 # monthly discount rate ~ 12.7% annually
    )
    return CLT

print(bgf_load(4,300,20,30))
print(ggf_load([4],[300],[20],[100]))