from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import requests
import copy

from backend.ml.model import predict_polygon
from backend.weather import get_weather_info
from backend.ml.llm import make_recommendation

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

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/recommendations")
async def recommendations(time_to_fire: int = 0):
    if time_to_fire == 0:
        raise HTTPException(status_code=400)
    return make_recommendation(time_to_fire)

@app.get("/wildfires")
async def wildfires():
    response = requests.get(URL)
    
    if response.status_code == 200:
        wildfires = response.json()
    else:
        return {"error": "fetching weather data"}
        
    weather_df = get_weather_info()
        
    # Include predictions from wildfire data
    predictions = [wildfires] 

    for day in range(3):
        predicted_object = copy.deepcopy(predictions[-1])
        predicted_fires = []
        for fire in predictions[-1]["features"]:
            predicted_fire = copy.deepcopy(fire)
            predicted_rings = []
            rings = fire["geometry"]["rings"]
            for ring in rings:
                predicted_rings.append(predict_polygon(
                    weather_df.iloc[day, 1],
                    weather_df.iloc[day, 2],
                    weather_df.iloc[day, 3],
                    ring
                ))
            # pdb.set_trace()
            predicted_fire["geometry"]["rings"] = predicted_rings
            predicted_fires.append(predicted_fire)
        predictions.append(predicted_object)
    
    return predictions