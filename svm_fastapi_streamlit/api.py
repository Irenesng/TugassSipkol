from fastapi import FastAPI
from pydantic import BaseModel

import pickle
import numpy as np

app = FastAPI()

model = pickle.load(open("model.pkl","rb"))
scaler = pickle.load(open("scaler.pkl","rb"))

class InputData(BaseModel):

    features:list

@app.get("/")
def home():

    return {"status":"SVM API Running"}

@app.post("/predict")
def predict(data:InputData):

    x=np.array(data.features).reshape(1,-1)

    x=scaler.transform(x)

    prediction=model.predict(x)[0]

    probability=model.predict_proba(x).max()

    return{

        "prediction":int(prediction),
        "probability":float(probability)

    }
