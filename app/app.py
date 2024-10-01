from fastapi import FastAPI
from pydantic import BaseModel
from lifetimes import BetaGeoFitter 

app = FastAPI()

class InputData(BaseModel):
    frequency: int
    recency: int
    T: int

@app.post("/predict")
def predict(data: InputData):
    try:
        bgf = BetaGeoFitter()
        bgf.load_model('../models/bgf_small_size.pkl')
        t = 1
        prediction = bgf.conditional_expected_number_of_purchases_up_to_time(t, frequency, recency, T)
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
