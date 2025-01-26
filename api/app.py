from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import json
import requests

URL = f"https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/WFIGS_Interagency_Perimeters_Current/FeatureServer/0/query?where=1%3D1&outFields=poly_IncidentName,poly_FeatureCategory,poly_DeleteThis,poly_FeatureAccess,poly_FeatureStatus,poly_IsVisible,poly_PolygonDateTime,attr_ContainmentDateTime,attr_ControlDateTime,attr_FireCause,attr_IncidentName,attr_IncidentShortDescription,attr_PercentContained&outSR=4326&f=json"

URL2 = "https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/Historic_GeoMAC_Perimeters_2019/FeatureServer/0/query?where=1%3D1&outFields=fireyear,incidentname&outSR=4326&f=json"

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

with open("data.json", "r") as file:
    data = json.load(file)
    wildfires = data["features"]

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/wildfires")
async def wildfires():
    response = requests.get(URL)
    
    if response.status_code == 200:
        data = response.json()
        return data["features"]
    else:
        print("An error occurred while fetching XWeather data")
        
    return {"status": "error"}

@app.get("/predict")
async def predict():
    return {"message": "Here is your prediction"}