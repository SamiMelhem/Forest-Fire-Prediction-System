from os import getenv
from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
from pydantic import BaseModel, ValidationError

load_dotenv()
client = OpenAI(
    api_key=getenv("OPENAI_API_KEY"),
)

AMBEE_API_KEY = getenv("AMBEE_API_KEY")
place = "Los Angeles"
base_url = "https://api.ambeedata.com/fire/latest/by-place"
params = {
    "place": place,
    "type": "reported"
}
headers = {
    "x-api-key": AMBEE_API_KEY
}
response = requests.get(base_url, params=params, headers=headers)
ambee_json = response.json()

ambee_str = json.dumps(ambee_json, indent=2)

class FireSummary(BaseModel):
    place: str
    summary: str
    # Add more fields if you want a more complex structure

# RAG where is the nearest evacuation center
system_prompt = (
    "You are a helpful assistant. You have the following fire data from Ambee:\n"
    f"{ambee_str}\n\n"
    "Please summarize the current fire situation and the nearest evacuation center for <the place>. "
    "Always respond in JSON format only. "
    "Your JSON schema is:\n"
    "{\n"
    '  "place": "<the place>",\n'
    '  "summary": "<your text summary>"\n'
    "}\n"
    "Do not include any extra keys or text outside the JSON."
)

chat_completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"Summarize the fire data for {place} with no extra text."
        },
    ],
)

raw_output = chat_completion.choices[0].message.content
print("Raw GPT response:\n", raw_output)

try:
    parsed_json = json.loads(raw_output)
except json.JSONDecodeError:
    print("GPT did not return valid JSON. Full response:\n", raw_output)
    raise

try:
    structured_output = FireSummary(**parsed_json)
except ValidationError as e:
    print("GPT JSON does not match the FireSummary schema:\n", e)
    raise

print("\nStructured LLM Output (Pydantic object):")
print(structured_output)

print("\nAccessing fields individually:")
print("place =", structured_output.place)
print("summary =", structured_output.summary)