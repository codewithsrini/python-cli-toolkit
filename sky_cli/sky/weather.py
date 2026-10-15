from .http_client import get_json
from .models import CurrentWeather, Forecast, Location, parse_daily

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

CURRENT_FIELDS = "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code"
DAILY_FIELDS = "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max"

def fetch_forecast(location: Location, days: int = 3, units: str = "metric") -> Forecast:
    """Fetch current conditions and a'days' -day forecast for a location. """

    params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "current": CURRENT_FIELDS,
        "daily": DAILY_FIELDS,
        "forcast_days": days,
        "timezone": "auto",
    }

    if units == "imperial":
        params["temperature_unit"] = "fahrenheit"
        params["wind_speed_unit"] = "mph"

    data = get_json(FORECAST_URL, params, service="weather service")

    return Forecast(
        location=location,
        current=CurrentWeather.from_api(data["current"]),
        daily=parse_daily(data["daily"]),
        units=units,
    )
