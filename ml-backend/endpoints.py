from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi import FastAPI, Request
import logging
import time

app = FastAPI()
# Loads the RandomForest model (rf_model.pkl) only once at startup (better performance than loading on every request).
model = joblib.load('../models/rf_model.pkl')
print("Model loaded successfully!")

# Defining input schema
# Pydantic automatically:
# Validates types (must be integers here)
# Produces helpful error messages if input is wrong
class Features(BaseModel):
    hour: int
    day_of_week: int
    transactionsCount: int
    gasUsed: int
    tokenTransfersCount: int
    totalTokenAmount: int
    uniqueSenders: int
    uniqueReceivers: int

logging.basicConfig(level=logging.INFO) # Allows logging of info-level events to stdout

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    logging.info(f"{request.method} {request.url} completed_in={process_time}s status_code={response.status_code}")
    return response

# Runs before and after every request.
# Measures how long a request took to process.
# Logs HTTP method, URL, duration, and HTTP status code.

# FastAPI automatically parses JSON into a Features object.
# The input values are converted to a NumPy array matching the model’s expected shape (1, 8).
# The model (RandomForestClassifier or Regressor) makes a prediction.
# The first (and only) prediction is returned as an integer in JSON format.
@app.post('/predict')
async def predict(features: Features):
    feature_vector = np.array([[
        features.hour,
        features.day_of_week,
        features.transactionsCount,
        features.gasUsed,
        features.tokenTransfersCount,
        features.totalTokenAmount,
        features.uniqueSenders,
        features.uniqueReceivers
    ]])
    prediction = model.predict(feature_vector)[0]
    return {"prediction": int(prediction)}
# curl -X POST http://localhost:3000/predict 
#   -H "Content-Type: application/json" 
    # -d '{"blockNumber":1,"hour":10,"day_of_week":3,"transactionsCount":10,"gasUsed":10000,"tokenTransfersCount":0,"totalTokenAmount":0,"uniqueSenders":0,"uniqueReceivers":0}'


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000) # runs the app using Uvicorn server.
