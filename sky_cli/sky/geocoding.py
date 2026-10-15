from .errors import LocationNotFoundError
from .http_client import get_json
from .models import Location

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

def search_locations(city: str, count: int = 5) -> list[Location]:
    """Return up to `count` places matching `city`, best match first."""
    params = {"name": city, "count": count, "language": "en", "format": "json"}

    data = get_json(GEOCODING_URL, params=params, service="location service")
    results = data.get("results", [])

    if not results:
        raise LocationNotFoundError(f"No place found matching '{city}'.")

    # Applying Comprehension
    return [Location.from_api(item) for item in results]
