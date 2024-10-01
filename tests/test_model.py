import unittest
from lifetimes import BetaGeoFitter

def test_model_training():
    try:
        df = pd.read_csv('../data/bgf_data.csv')
        bgf = BetaGeoFitter(penalizer_coef=3.001)
        bgf.fit(data_f['frequency'], data_f['recency'], data_f['T'])
        bgf.save_model('../models/ggf_small_size.pkl', save_data=False, save_generate_data_method=False)
        print(bgf)
    assert
            