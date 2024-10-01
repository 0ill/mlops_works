import unittest
from lifetimes import BetaGeoFitter
import pandas as pd

def test_model_training():
    try:
        df = pd.read_csv('data/bgf_data.csv').head(300)
        bgf = BetaGeoFitter()
        bgf.load_model('models/bgf_small_size.pkl')
        t = 3
        cen = bgf.predict(t, df['frequency'], df['recency'], df['T'])
        print(cen)
    except Exception as e:
        print(e)
        
test_model_training()          