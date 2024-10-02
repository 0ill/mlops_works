from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from lifetimes import BetaGeoFitter 


class InputData(BaseModel):
    frequency: float
    recency: float
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
    bgf = BetaGeoFitter()
    bgf.load_model('../models/bgf_small_size.pkl')
    prediction = bgf.predict(t, frequency, recency, T)
    return {'prediction':prediction}

if __name__ == '__main__':
    uvicorn(app,host ='127.0.0.1', port =8000)