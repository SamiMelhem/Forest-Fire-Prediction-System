from os import getenv
import json
import boto3
from pydantic import BaseModel

class WildfireAdvice(BaseModel):
    recommendations: str

boto3.setup_default_session(
    aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"), 
    aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=getenv("AWS_SESSION_TOKEN"),
    region_name='us-west-2'
)
bedrock_client = boto3.client(service_name="bedrock-runtime")

severity_guidelines = """
We have three tiers of severity based on the size of fires and distance:

LOW SEVERITY
- Limit outdoor exposure / Stay indoors
- Use Air purifiers
- Keep medications accessible

MODERATE SEVERITY
- Wear N95 or P100 masks
- Seal windows; avoid candles & gas stoves
- Monitor real-time wind shifts; have evacuation kit ready

HIGH SEVERITY
- Evacuate immediately when ordered
- Secure home utilities

"""
size_of_fire, distance_of_fire = 20, 20
input_data = f"""
Size of fire: Abs(Lat.-Lon.) = {size_of_fire} miles
Distance from fire: Euclidean Distance(Lat.-Lon.) = {distance_of_fire} miles
"""

system_message = f"""You are a helpful wildfire assistant, referencing institutional guidelines
(NFPA, OSFM, DOI, Community Wildfire Planning Center, etc.) for recommendations. 

Here is an overview of severity-based recommendations:
{severity_guidelines}

Input:
{input_data}

Your task:
- Provide the user with location-specific advice for the next 7 days (List only the most important recommendations based on the input data)
- No code, just advice based on the input data (Should be one of the severities)
- Output ONLY valid JSON with this schema (Starting and Ending with this exact JSON format):
{{
  "recommendations": "<the text-based recommendations>"
}}
No extra keys, no extra text. 
"""

body_dict = {
    "prompt": system_message,
    "max_gen_len": 512,
    "temperature": 0.5,
    "top_p": 0.9
}
payload = {
    "modelId": "meta.llama3-1-405b-instruct-v1:0",
    "contentType": "application/json",
    "accept": "application/json",
    "body": json.dumps(body_dict)
}
response = bedrock_client.invoke_model(
    modelId=payload["modelId"],
    contentType=payload["contentType"],
    accept=payload["accept"],
    body=payload["body"]
)
response_body = response["body"].read().decode("utf-8")
print(response_body)