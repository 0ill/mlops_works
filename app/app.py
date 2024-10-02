from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pandas as pd
from lifetimes import BetaGeoFitter 
from lifetimes import GammaGammaFitter


class InputData(BaseModel):
    frequency: float
    recency: float
    amt: float
    T: float
    t: int

app = FastAPI()

@app.get('/')
def hello():
    return {"message": "hello world !"}

@app.post("/predict")
def predict(data: InputData):
    data = data.dict()
    frequency = data['frequency']
    t = data['t']
    recency = data['recency']
    T = data['T']
    monetary_value = data['amt']
    bgf = BetaGeoFitter()
    bgf.load_model('../models/bgf_small_size.pkl')
    prediction = bgf.predict(t, frequency, recency, T)
    ggf = GammaGammaFitter()
    ggf.load_model('models/ggf_small_size.pkl')
    ceap = ggf.conditional_expected_average_profit(frequency,frequency)
    df = pd.DataFrame()
    df['frequency'] = [frequency]
    df['recency'] = [recency]
    df['T'] = [T]
    df['monetary_value'] = [monetary_value]
    CLT = ggf.customer_lifetime_value(
        bgf,
        df['frequency'],
        df['recency'],
        df['T'],
        df['monetary_value'],
        time=t, # months
        discount_rate=0.00 # monthly discount rate ~ 12.7% annually
    )
    return {'expected actions':prediction,
            'life time value': CLT,
            'avg profit': ceap
            }

if __name__ == '__main__':

    uvicorn(app,host ='127.0.0.1', port =8000)