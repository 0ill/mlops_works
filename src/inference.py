import pandas as pd
import numpy as np
from lifetimes import BetaGeoFitter 
from lifetimes import GammaGammaFitter

def bgf_load():
    bgf = BetaGeoFitter
    bgf.load_model('../models/bgf_small_size.pkl')
    return bgf

def ggf_load():
    ggf = GammaGammaFitter
    ggf.load_model('../models/ggf_small_size.pkl')
    return ggf