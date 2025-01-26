from openmeteo_requests import Client
from requests_cache import CachedSession
from pandas import DataFrame, date_range, to_datetime, Timedelta
from retry_requests import retry

cache_session = CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = Client(session = retry_session)

url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 34.052235, # LA Coord
	"longitude": -118.243683, # LA Coord
	"hourly": ["temperature_2m", "wind_speed_10m", "wind_direction_10m"],
    "wind_speed_unit": "ms",
    "forecast_days": 3
}
responses = openmeteo.weather_api(url, params=params)

# --- Process the first location ---
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")

# --- Process hourly data ---
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy() + 273.15
hourly_wind_speed_10m = hourly.Variables(1).ValuesAsNumpy()
hourly_wind_direction_10m = hourly.Variables(2).ValuesAsNumpy()

# Create a time index for each hourly observation
hourly_data = {
    "date": date_range(
        start=to_datetime(hourly.Time(), unit="s", utc=True),
        end=to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ),
    "temperature_2m": hourly_temperature_2m,
    "wind_speed_10m": hourly_wind_speed_10m,
    "wind_direction_10m": hourly_wind_direction_10m
}

hourly_dataframe = DataFrame(data=hourly_data)
print("\nHourly dataframe:\n", hourly_dataframe.head(24)) 
hourly_dataframe['day'] = hourly_dataframe['date'].dt.date

hourly_dataframe.rename(columns={
    "temperature_2m": "temperature (K)",
    "wind_speed_10m": "wind_speed (m/s)",
    "wind_direction_10m": "wind_direction (°)"
}, inplace=True)

daily_means = hourly_dataframe.groupby('day').agg({
    'temperature (K)': 'mean',
    'wind_speed (m/s)': 'mean',
    'wind_direction (°)': 'mean'
}).reset_index()

print("\nDaily averages:\n", daily_means)