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
    return [
        [
            (-121.6368879649432, 36.130093599936025),
            (-121.63643144071087, 36.14113352808071),
            (-121.64336774918961, 36.154276375241736),
            (-121.65219978535809, 36.16482305070381),
            (-121.66059894586652, 36.17180414483178),
            (-121.66458441676862, 36.174459164870235),
            (-121.6630628482444, 36.17799137753191),
            (-121.65548150999547, 36.18658812474986),
            (-121.6464462410827, 36.19319427363452),
            (-121.63659443029579, 36.19150853894524),
            (-121.6284659743937, 36.18469968823104),
            (-121.61925135301563, 36.17621055892247),
            (-121.60975515017326, 36.16961071283867),
            (-121.60023266492135, 36.165183407836324),
            (-121.59024691863537, 36.15975142677288),
            (-121.58379467142834, 36.15245468309288),
            (-121.57469007597008, 36.14716732265376),
            (-121.56529875734348, 36.14389420227302),
            (-121.56028301717826, 36.14464484850578),
            (-121.55527279054502, 36.14556645834803),
            (-121.55130533896251, 36.14162463483416),
            (-121.54911440907976, 36.13495732033047),
            (-121.55013673862953, 36.132069293857256),
            (-121.54915216296537, 36.12835776753704),
            (-121.5441827192725, 36.11814421096461),
            (-121.536507729094, 36.107495557401705),
            (-121.52759004497592, 36.09842735572893),
            (-121.51551625968699, 36.09104557113433),
            (-121.50835113131049, 36.082687789833805),
            (-121.50143912582185, 36.07664235399446),
            (-121.49509076752992, 36.070711503815296),
            (-121.48996975835692, 36.06205426652426),
            (-121.49311252721246, 36.053505697501954),
            (-121.49896223518262, 36.047602380962594),
            (-121.50697186162908, 36.03998580492258),
            (-121.51539315568199, 36.03445018022128),
            (-121.52580950463599, 36.036880622520734),
            (-121.53647033541168, 36.04075700813542),
            (-121.54747173105923, 36.042087681340085),
            (-121.55814075479589, 36.04291847986552),
            (-121.56897573517776, 36.046018961574084),
            (-121.57709822792818, 36.04943008019892),
            (-121.58687937224326, 36.057663092147045),
            (-121.5940396945989, 36.06593387615573),
            (-121.59966610762618, 36.07511786337941),
            (-121.60464365725116, 36.08561169851222),
            (-121.61241585584477, 36.0958800251328),
            (-121.62278813225306, 36.1042174208115),
            (-121.63250290054056, 36.11485960194996),
            (-121.63688796494318, 36.13009359993603),
            (-121.6368879649432, 36.130093599936025)
        ],
    ]