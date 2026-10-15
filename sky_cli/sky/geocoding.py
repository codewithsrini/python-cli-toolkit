import requests
import json

from .errors import LocationNotFoundError, WeatherSercviceError
from .models import Location

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
TIMEOUT_SECONDS = 10

def search_locations(city: str, count: int = 5) -> list[Location]:
    """Return up to `count` places matching `city`, best match first."""
    params = {"name": city, "count": count, "language": "en", "format": "json"}

    try:
        response = requests.get(GEOCODING_URL, params=params, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.Timeout as e:
        raise WeatherSercviceError("The location service took too long to respond") from e
    except requests.RequestException as e:
        raise WeatherSercviceError(f"Could not reach the location service: {e}") from e

    data = response.json()
    results = data.get("results", [])

    if not results:
        raise LocationNotFoundError(f"No place found matching '{city}'.")

    # print(json.dumps(results, indent=4))

    # Old way of iterating
    # for loc in results:
    #     location = Location(
    #         name=loc.get("name", ""),
    #         latitude=loc.get("latitude", ""),
    #         longitude=loc.get("longitude", ""),
    #         region=loc.get("admin1", None),
    #         country=loc.get("country", ""),
    #     )

    #     locations.append(location)
    
    # return locations

    # Applying Comprehension
    return [Location.from_api(item) for item in results]
